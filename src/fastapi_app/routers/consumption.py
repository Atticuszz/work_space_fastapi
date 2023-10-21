# coding=utf-8
import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, Form, File

from src.fastapi_app.data_base.client import supabase_client
from src.fastapi_app.dependencies import unzip_file, read_and_filter

router_consumption = APIRouter()


@router_consumption.get("/get_all_consumption")
async def get_all_consumption() -> dict:
    data = await supabase_client.get_table("consumption")
    return data


@router_consumption.post("/update_consumption")
async def update_consumption(file: UploadFile = File(...), password: str = Form(None)):
    # First, save the uploaded file
    temp_file = Path(file.filename)

    with temp_file.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    csv_file: Path = unzip_file(temp_file, password)
    csv_df = read_and_filter(csv_file)
    # let csv_df to be dict
    bill_json: list[dict] = csv_df.to_dict("records")
    await supabase_client.multi_requests("consumption", bill_json, "upsert")
    # 清楚临时文件
    csv_file.unlink()
    csv_file.parent.rmdir()
    return {"message": "Successfully processed the uploaded file"}
