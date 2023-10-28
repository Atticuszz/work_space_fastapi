# coding=utf-8

from fastapi import APIRouter

from src.fastapi_app.data_base.client import supabase_client

router_task_categories = APIRouter()


@router_task_categories.get("/get_all_task_category")
async def get_all_task_category() -> dict:
    page_data = await supabase_client.get_table("single_page")
    task_category = page_data[0]
    # pprint.pprint(task_category)
    return task_category


# New route to delete a category


@router_task_categories.put("/update_category")
async def update_category(data: dict | None = None):
    updated_data = await supabase_client.upsert("single_page", data)
    return updated_data
