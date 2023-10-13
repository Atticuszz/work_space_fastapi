# coding=utf-8
import timeit

from dotenv import load_dotenv

from src.supabase.client_async import create_client  # 假设这是你的异步Supabase客户端

load_dotenv()


async def fetch_data(client):
    return await client.table("task_done_list").select("*").execute()


async def my_test(times: int = 10):
    # 获取环境变量
    url = "https://nbmadjuchetpciiqvqyv.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5ibWFkanVjaGV0cGNpaXF2cXl2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTY5OTQyMDgsImV4cCI6MjAxMjU3MDIwOH0.TeOs98Og9atir4CGmT5QIEPNhH6lRvpx_KaGl0JBvcA"

    # 创建客户端
    client = create_client(url, key)

    # 初始化用于计时的变量
    total_time = 0

    # 存储所有的异步任务
    tasks = []

    # 记录开始时间
    start_time = timeit.default_timer()

    # 创建1000个请求任务
    for _ in range(times):
        print("fetching data {} times".format(_))
        task = asyncio.ensure_future(fetch_data(client))
        tasks.append(task)

    # 等待所有任务完成
    responses = await asyncio.gather(*tasks)

    # 记录结束时间并计算总耗时
    end_time = timeit.default_timer()
    total_time = end_time - start_time

    # 计算平均耗时
    avg_time = total_time / times

    print(f"Total time for 1000 requests: {total_time} seconds.")
    print(f"Average time per request: {avg_time} seconds.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(my_test())
