import asyncio
import csv
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .data_base import supabase_client

__all__ = ["fastapi_scheduler"]


async def backup_data():
    """
    Backup data from supabase in CSV format
    """
    try:
        # Define directory where backup CSV files will be stored
        csv_dir = Path(__file__).parents[1] / "backup" / "supabase_tables"
        csv_dir.mkdir(parents=True, exist_ok=True)  # Create dir if it doesn't exist

        # List of table names to back up
        for table_name in ["task_done_list", "single_page", "consumption"]:
            # Fetch data from Supabase table
            table_data = await supabase_client.get_table(table_name)

            if table_data:
                # Define the CSV file path
                csv_file = csv_dir / f"{table_name}.csv"

                # Writing to csv file
                with open(csv_file, 'w', newline='', encoding="utf-8") as csvfile:
                    # Create a CSV writer object
                    csvwriter = csv.writer(csvfile)

                    # Write the header
                    headers = table_data[0].keys()
                    csvwriter.writerow(headers)

                    # Write the data
                    for row in table_data:
                        csvwriter.writerow(row.values())
            else:
                print(f"Failed to get data for table {table_name}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to run backup_data in a new event loop
def sync_back_up():
    asyncio.new_event_loop().run_until_complete(backup_data())


# Initialize the APScheduler
fastapi_scheduler = BackgroundScheduler()

# Add a job to run backup_data every 5 minutes
fastapi_scheduler.add_job(
    func=sync_back_up,
    trigger=IntervalTrigger(minutes=10),
    id='backup_job',
    name='Backup Supabase data every 10 minutes',
    replace_existing=True
)
