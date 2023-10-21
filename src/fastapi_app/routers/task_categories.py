# coding=utf-8

from fastapi import APIRouter

from src.fastapi_app.data_base.client import supabase_client

router_task_categories = APIRouter()


@router_task_categories.get("/get_all_task_category")
async def get_all_task_category() -> dict:
    page_data = await supabase_client.get_table("single_page", columns=['category', 'task', 'target', 'location'])
    task_category = page_data[0]
    # pprint.pprint(task_category)
    return task_category


# New route to delete a category


@router_task_categories.put("/update_category/{list_name}")
async def update_category(list_name: str, data: dict | None = None):
    page_data = await supabase_client.get_table("single_page")
    existing_data = page_data[0][list_name]
    # print("existing_data:", existing_data)
    # print("data:", data)
    if list_name in page_data[0]:
        if data.get('add', None):
            existing_data.append(data['add'])
        else:
            existing_data.remove(data['remove'])
    page_data[0][list_name] = existing_data
    # print("page_data:", page_data[0])
    updated_data = await supabase_client.upsert("single_page", page_data[0])
    return updated_data
