# coding=utf-8

from fastapi import APIRouter

from my_app.model import TaskDoneEntry
from my_app.strapi_cmd_starter import strapi_restful
from my_app.tools import entries_sort_key

router_task_entries = APIRouter()





@router_task_entries.get("/get_all_table_items")
async def get_all_table_items() -> list[dict]:
    entries = await strapi_restful.get_entries("task-done-lists", get_all=True)
    entries_data = [entry['attributes'] for entry in entries['data']]
    entries_data.sort(key=entries_sort_key, reverse=True)
    # pprint.pprint(entries_data)
    return entries_data


@router_task_entries.post("/add_entry")
async def add_entry(data: TaskDoneEntry):
    print("add_entry:", data.model_dump())
    new_entry = await strapi_restful.create_entry("task-done-lists", data.model_dump())

    return new_entry


@router_task_entries.put("/update_entry/{uuid}")
async def update_entry(uuid: str, data: TaskDoneEntry):
    # 更新条目
    filters = {'uuid': {'$eq': uuid}}
    entries = await strapi_restful.get_entries("task-done-lists", filters=filters)
    if not entries['data']:
        return {"error": "Entry not found"}
    else:
        print("update_entry:", entries['data'])
    document_id = entries['data'][0]['id']
    updated_entry = await strapi_restful.update_entry("task-done-lists", document_id, data.model_dump())
    return updated_entry


@router_task_entries.delete("/delete_entry/{uuid}")
async def delete_entry(uuid: str):
    # 删除条目
    filters = {'uuid': {'$eq': uuid}}
    entries = await strapi_restful.get_entries("task-done-lists", filters=filters)
    if not entries['data']:
        return {"error": "Entry not found"}
    else:
        print("delete_entry:", entries['data'])
    document_id = entries['data'][0]['id']
    deleted_entry = await strapi_restful.delete_entry("task-done-lists", document_id)
    return deleted_entry
