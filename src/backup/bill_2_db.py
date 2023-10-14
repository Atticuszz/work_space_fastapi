# coding=utf-8
from datetime import datetime
from pathlib import Path

import pandas as pd
from pandas import Timedelta
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, Field, create_engine, Session

from src.metabase.bill_clean import read_and_filter
from src.metabase.bill_clean import unzipper


class Transaction(SQLModel, table=True):
    Order_id: str = Field(primary_key=True)  # 新增的主键字段
    Transaction_Time: datetime
    Transaction_Partner: str
    Primary_Category: str
    Secondary_Category: str
    Product: str
    Amount: float


class TransactionDB:
    """
    A class to handle SQLite database.
    """

    def __init__(self, db_name: str, table_name: str):
        self.engine = create_engine(f"sqlite:///{db_name}")
        self.table_name = table_name
        self.session = Session(self.engine)
        SQLModel.metadata.create_all(self.engine)

    def drop_duplicates(self, csv_df: pd.DataFrame):
        # Drop duplicates based on 'Order_id'
        duplicate_rows = csv_df[csv_df.duplicated(
            subset=['Order_id'], keep=False)]
        assert duplicate_rows.empty, f"Duplicate Order_ids found: {duplicate_rows}"

        # Check for duplicates in 'Transaction_Time'
        duplicate_time_rows = csv_df[csv_df.duplicated(
            subset=['Transaction_Time'], keep=False)].sort_values('Transaction_Time')

        if not duplicate_time_rows.empty:
            # Make 'Transaction_Time' unique by adding 1 second to duplicates
            correction = Timedelta(seconds=1)
            seen = {}  # Dictionary to keep track of duplicate times

            for idx, row in duplicate_time_rows.iterrows():
                time = row['Transaction_Time']
                if time in seen:
                    seen[time] += 1
                    new_time = time + (correction * seen[time])
                    csv_df.at[idx, 'Transaction_Time'] = new_time
                else:
                    seen[time] = 0  # Initialize count

        return csv_df

    def update_or_ask(self, conflicting_records) -> int:
        update_num = 0
        if conflicting_records:
            print("以下数据有冲突：")
            for existing, new in conflicting_records:
                # 打印必须的 订单号和交易时间
                print(
                    f"订单号: {existing['Order_id']}, 交易时间: {existing['Transaction_Time']}")
                print_conflicting_fields(existing, new)  # 使用定义的函数
                update_num += 1

            choice = input("是否要覆盖这些记录？(y/n): ")
            if choice.lower() == 'y':
                for existing, new in conflicting_records:
                    existing_record = self.session.query(Transaction).filter_by(
                        Order_id=existing['Order_id']).first()
                    for key, value in new.items():
                        setattr(existing_record, key, value)
                self.session.commit()
        return update_num

    def bill_to_db(self, csv_df: pd.DataFrame):
        # Drop duplicates within the CSV itself based on 'Order_id'
        csv_df = self.drop_duplicates(csv_df)

        if not csv_df.empty:
            record_list = csv_df.to_dict(orient='records')
            conflicting_records = []  # To hold conflicting records
            add_num: int = 0
            with self.session:
                for record in record_list:
                    existing_record = self.session.query(Transaction).filter_by(
                        Order_id=record['Order_id']).first()

                    if existing_record:
                        # Convert SQLAlchemy object to dictionary
                        existing_dict = {
                            column.name: getattr(
                                existing_record,
                                column.name) for column in Transaction.__table__.columns}
                        if existing_dict != record:
                            # If the existing and new records are not the same,
                            # add to conflict list
                            conflicting_records.append((existing_dict, record))
                    else:
                        # If the record does not exist in the database, add it
                        new_record = Transaction(**record)
                        self.session.add(new_record)
                        add_num += 1

                # After the loop, handle conflicts
                update_num: int = self.update_or_ask(conflicting_records)

                try:
                    self.session.commit()
                    print(f"Successfully added {add_num} records")
                    print(f"Successfully updated {update_num} records")
                except IntegrityError as e:
                    print(f"Database insertion error: {e}")
                    self.session.rollback()  # Rollback the transaction

    def db_to_csv(self, output_file: str):
        """
        Export data from SQLite database to a CSV file using pandas.

        Parameters:
        - output_file (str): The name of the output CSV file.
        """
        # Create a query string
        query = self.session.query(Transaction).statement

        # Read SQL query into a DataFrame
        df = pd.read_sql(query, self.session.bind)
        # 确保没有重复数据，根据order_id判断
        df = self.drop_duplicates(df)

        # Export DataFrame to CSV
        df.to_csv(output_file, index=False)
        print(f"Data has been exported to {output_file}")


def print_conflicting_fields(existing: dict, new: dict):
    print("Conflicting Fields:")
    for key in existing.keys():
        if existing[key] != new[key]:
            print(f"Field: {key}, Existing: {existing[key]}, New: {new[key]}")


def conbine_csv(db_name: str, table_name: str):
    unzipper.unzip_files()

    db = TransactionDB(db_name, table_name)

    for csv_path in Path.cwd().joinpath('bill_csv').glob('*.csv'):
        db.bill_to_db(read_and_filter(csv_path))


if __name__ == '__main__':
    db_name = 'Atticus_work_place.db'
    table_name = 'transaction'
    db = TransactionDB(db_name, table_name)
    Path('bill_csv').mkdir(exist_ok=True)
    db.db_to_csv('bill_csv/bill.csv')
