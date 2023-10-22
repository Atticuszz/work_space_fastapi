# coding=utf-8

from fastapi import APIRouter

from src.fastapi_app.data_base.client import supabase_client
from src.fastapi_app.model import TaskDoneEntry
from src.fastapi_app.tools import entries_sort_key

router_task_entries = APIRouter()


@router_task_entries.get("/get_all_table_items")
async def get_all_table_items() -> list[dict]:
    entries = await supabase_client.get_table("task_done_list")
    # print(entries)
    entries.sort(key=entries_sort_key, reverse=True)
    # pprint.pprint(entries_data)
    return entries


@router_task_entries.post("/upsert_entry")
async def upsert_entry(data: TaskDoneEntry):
    # print("add_entry:", data.model_dump())
    new_entry = await supabase_client.upsert("task_done_list", data.model_dump())
    return new_entry



@router_task_entries.delete("/delete_entry/{uuid}")
async def delete_entry(uuid: str):
    deleted_entry = await supabase_client.delete("task_done_list", uuid)
    return deleted_entry
