from pydantic import BaseModel


# coding=utf-8
class TaskDoneEntry(BaseModel):
    uuid: str
    date: str
    category: list[str]
    task: list[str]
    detail: str
    slot: str
    location: str