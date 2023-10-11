# coding=utf-8

import os
from dotenv import load_dotenv
from postgrest import APIResponse
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions

load_dotenv()


class SupaBase:
    def __init__(self, url: str = os.getenv("SUPABASE_URL"),
                 key: str = os.getenv("SUPABASE_KEY")):

        self.client: Client = create_client(url, key, options=ClientOptions(
            postgrest_client_timeout=10,
            storage_client_timeout=10
        ))
    def get_table(self, name: str):
        response: APIResponse = self.client.table(name).select("*").execute()
        return response.data


if __name__=="__main__":
    client = SupaBase()
    print(client.get_table("task_done_list"))
