from pathlib import Path

import pandas as pd
from pandas import Timedelta


def drop_duplicates(csv_df: pd.DataFrame):
    # Drop duplicates based on 'order_id'
    duplicate_rows = csv_df[csv_df.duplicated(
        subset=['order_id'], keep=False)]
    assert duplicate_rows.empty, f"Duplicate order_id found: {duplicate_rows}"

    # Check for duplicates in 'Transaction_Time'
    duplicate_time_rows = csv_df[csv_df.duplicated(
        subset=['time'], keep=False)].sort_values('time')

    if not duplicate_time_rows.empty:
        # Make 'Transaction_Time' unique by adding 1 second to duplicates
        correction = Timedelta(seconds=1)
        seen = {}  # Dictionary to keep track of duplicate times

        for idx, row in duplicate_time_rows.iterrows():
            time = row['time']
            if time in seen:
                seen[time] += 1
                new_time = time + (correction * seen[time])
                csv_df.at[idx, 'time'] = new_time
            else:
                seen[time] = 0  # Initialize count

    return csv_df


def strip_in_data(df: pd.DataFrame):
    """
    Strip whitespace in column names and values.
    Args:
        df:

    Returns:

    """
    # Common data cleaning
    df.columns = df.columns.str.strip()
    df = df.map(
        lambda x: x if not isinstance(
            x, str) else x.strip())
    return df


def read_and_filter(csv_path: Path) -> pd.DataFrame:
    """
    Read and filter csv file.
    Args:
        csv_path:

    Returns:

    """
    tar_cols = [
        'order_id',
        'time',
        'merchant',
        'category_1',
        'category_2',
        'product',
        'cost',
    ]

    if csv_path.name.startswith("wechat"):
        csv_df = pd.read_csv(csv_path, header=16, encoding='utf-8')
        csv_df = strip_in_data(csv_df)
        order_id_key = '交易单号'
        time_key = '交易时间'
        product_key = '商品'
        amount_key = '金额(元)'  # 有英文括号
        condition = (
                            csv_df['收/支'] == '支出') & (csv_df['当前状态'].isin(['支付成功', '已转账', '对方已收钱']))
    else:
        csv_df = pd.read_csv(csv_path, encoding='gbk', skiprows=4).iloc[:-7]
        csv_df = strip_in_data(csv_df)
        order_id_key = '交易号'
        time_key = '付款时间'
        product_key = '商品名称'
        amount_key = '金额（元）'  # 有中文括号
        condition = ~csv_df['交易状态'].isin(['交易失败', '交易关闭', '退款成功'])
    mappings = {
        '交易对方': 'merchant',
        product_key: 'product',
        order_id_key: 'order_id',
    }

    # Filter
    csv_df = csv_df[condition]

    # Type conversion
    csv_df['time'] = csv_df[time_key].astype(
        'datetime64[ns]')

    if csv_df[amount_key].dtype == 'object':
        csv_df['cost'] = csv_df[amount_key
        ].str.replace('¥', '').astype('float64')
    else:
        csv_df['cost'] = csv_df[amount_key]

    csv_df['category_1'] = ''
    csv_df['category_2'] = ''

    csv_df = csv_df.rename(columns=mappings)
    # Drop duplicates by 'order_id',time
    csv_df = drop_duplicates(csv_df[tar_cols])
    # Convert 'time' to string for json serialization
    csv_df['time'] = csv_df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    return csv_df
