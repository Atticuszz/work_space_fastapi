# coding=utf-8
import asyncio
import os

from dotenv import load_dotenv
from postgrest import APIResponse

from src.supabase import create_client, AsyncClient
from src.supabase.lib.client_options import ClientOptions

load_dotenv()


class SupaBase:
    def __init__(self, url: str = os.getenv("SUPABASE_URL"),
                 key: str = os.getenv("SUPABASE_KEY")):
        self.client: AsyncClient = create_client(
            url, key, options=ClientOptions(
                postgrest_client_timeout=10, storage_client_timeout=10))

    async def get_table(self, name: str, columns: list[str] | None = None) -> list[dict]:
        if columns is None:
            columns = ["*"]
        select_params: str = ",".join(columns)
        response: APIResponse = await self.client.table(name).select(select_params).execute()
        return response.data

    async def upsert(self, name: str, data: dict) -> list[dict]:
        response: APIResponse = await self.client.table(name).upsert(data).execute()
        return response.data

    async def delete(self, name: str, uuid: str) -> list[dict]:
        response: APIResponse = await self.client.table(
            name).delete().eq("uuid", uuid).execute()
        return response.data


supabase_client = SupaBase()


async def main():
    data = await supabase_client.get_table("task_done_list")
    print(data)


if __name__ == "__main__":
    asyncio.run(main())
    # 将数据转换为json数据
