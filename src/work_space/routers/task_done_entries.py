# coding=utf-8

from fastapi import APIRouter

from src.work_space.data_base.client import supabase_client
from src.work_space.model import TaskDoneEntry
from src.work_space.tools import entries_sort_key

router_task_entries = APIRouter()


@router_task_entries.get("/get_all_table_items")
async def get_all_table_items() -> list[dict]:
    entries = await supabase_client.get_table("task_done_list")
    # print(entries)
    entries.sort(key=entries_sort_key, reverse=True)
    # pprint.pprint(entries_data)
    return entries


@router_task_entries.post("/add_entry")
async def add_entry(data: TaskDoneEntry):
    # print("add_entry:", data.model_dump())
    new_entry = await supabase_client.upsert("task_done_list", data.model_dump())
    return new_entry


@router_task_entries.put("/update_entry/{uuid}")
async def update_entry(uuid: str, data: TaskDoneEntry):
    updated_entry = await supabase_client.upsert("task_done_list", data.model_dump())
    return updated_entry


@router_task_entries.delete("/delete_entry/{uuid}")
async def delete_entry(uuid: str):
    deleted_entry = await supabase_client.delete("task_done_list", uuid)
    return deleted_entry
