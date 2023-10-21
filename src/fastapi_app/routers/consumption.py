# coding=utf-8
import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, Form, File

from src.fastapi_app.data_base.client import supabase_client
from src.fastapi_app.tools import unzip_file

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

    unzip_file(temp_file, password)

    # TODO: Now, you can read the CSV files from the destination directory

    return {"message": "Successfully processed the uploaded file"}
