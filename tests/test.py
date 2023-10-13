import asyncio
import timeit

from src.work_space.data_base.client import SupaBase

supabase_client = SupaBase()


async def calculate_time(n: int, funtion: callable, *args, **kwargs):
    tasks = []
    start_time = timeit.default_timer()

    for _ in range(n):
        task = asyncio.ensure_future(
            funtion(*args))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)

    end_time = timeit.default_timer()
    total_time = (end_time - start_time)
    average_time = total_time / n

    print(f"Total time for {n} requests: {total_time} seconds.")
    print(f"Average time per request: {average_time} seconds.")

    return total_time, average_time


def transform():
    data = supabase_client.get_table("task_done_list")
    keys = ['category', 'task']
    for key in keys:
        for item in data:
            str_data = item[key].strip("'").replace("[", '').replace("]", '')
            arr_data = str_data.split(',')
            item[key] = arr_data

    # update
    for i, item in enumerate(data):
        print(f"updating {i + 1}/{len(data)}")
        supabase_client.upsert("task_done_list", item)


async def transform2():
    data = await supabase_client.get_table("task_done_list")
    keys = ['category', 'task']
    for key in keys:
        for item in data:
            item[key] = [i.strip('"') for i in item[key]]
    tasks = [
        asyncio.ensure_future(
            supabase_client.upsert(
                "task_done_list",
                item)) for item in data]
    results = await asyncio.gather(*tasks)
    print("done:", results)


def upsert_data():
    # all_data = supabase_client.get_table("task_done_list")

    data = supabase_client.upsert(
        "task_done_list", {
            "uuid": "70edae09-7248-49db-a404-3cb71f0105e9", "task": []})
    return data


if __name__ == "__main__":
    asyncio.run(transform2())
    # asyncio.run(calculate_time(1000))
    # asyncio.run(calculate_time(10000))
    # asyncio.run(calculate_time(100000))
    # asyncio.run(calculate_time(1000000))
    # asyncio.run(calculate_time(10000000))
