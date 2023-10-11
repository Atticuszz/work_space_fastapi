# coding=utf-8
from fastapi import APIRouter

from my_app.strapi_cmd_starter import strapi_restful

router_task_categories = APIRouter()


@router_task_categories.get("/get_all_task_category")
async def get_all_task_category() -> dict:
    page_data = await strapi_restful.send_get_request("task-category")
    # pprint.pprint(page_data)
    task_category = page_data['data']['attributes']['category']
    return task_category


# New route to delete a category


@router_task_categories.delete("/update_category/{list_name}/{item}")
async def update_category(list_name: str, data: dict | None = None):
    page_data = await strapi_restful.send_get_request("task-category")
    existing_data = page_data['data']['attributes']['category']
    if list_name in existing_data:
        if data.get('add', None):
            existing_data.append(data['add'])
        else:
            existing_data.remove(data['remove'])
    updated_data = await strapi_restful.send_post_request("update_task_category", existing_data)
    return updated_data
