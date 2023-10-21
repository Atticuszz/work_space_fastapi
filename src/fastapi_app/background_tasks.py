# coding=utf-8
import asyncio
import json
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.fastapi_app.data_base.client import supabase_client


async def backup_data():
    """
    Backup data from supabase
    :return:
    """
    try:
        json_dir = Path(__file__).parents[1] / "backup" / "supabase_tables"
        json_dir.mkdir(parents=True, exist_ok=True)  # Create dir if not exists

        for table_name in ["task_done_list", "single_page", "consumption"]:
            table_data = await supabase_client.get_table(table_name)
            if table_data:
                json_file = json_dir / f"{table_name}.json"
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(table_data, f)
            else:
                print(f"Failed to get data for table {table_name}")
    except Exception as e:
        print(f"An error occurred: {e}")


def sync_back_up():
    asyncio.new_event_loop().run_until_complete(backup_data())


fastapi_scheduler = BackgroundScheduler()
fastapi_scheduler.add_job(
    func=sync_back_up,
    trigger=IntervalTrigger(minutes=10),  # Change to 300 seconds (5 minutes)
    id='backup_job',
    name='Backup Supabase data every 5 minutes',  # Changed the name
    replace_existing=True
)
