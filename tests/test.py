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


async def safe_upsert(item, retries=3):
    for i in range(retries):
        try:
            await supabase_client.upsert(data=item, name="task_done_list")
            return
        except Exception as e:
            print(f"An error occurred: {e}. Retrying... ({i + 1}/{retries})")
            await asyncio.sleep(0.001)


async def multi_requests(data: list):
    # with open("test_data.json", "r") as f:
    #     data = json.load(f)
    chunk_size = 4000
    for i in range(0, len(data), chunk_size):
        chunk_data = data[i:i + chunk_size]
        tasks = [
            asyncio.ensure_future(
                safe_delete(
                    item["uuid"])) for item in chunk_data]
        # tasks = [asyncio.ensure_future(safe_upsert(item))
        # for item in chunk_data]
        await asyncio.gather(*tasks)
    return


async def safe_delete(uuid: str, retries: int = 3):
    for i in range(retries):
        try:
            await supabase_client.delete(uuid=uuid, name="task_done_list")
            return
        except Exception as e:
            print(f"An error occurred: {e}. Retrying... ({i + 1}/{retries})")
            await asyncio.sleep(0.001)
    return


async def data_2_del():
    data = await supabase_client.get_table("task_done_list")
    data.sort(
        key=lambda x: x["createdAt"] if isinstance(
            x["createdAt"],
            str) else "")
    data_2_del = data[34:]
    await multi_requests(data_2_del)


if __name__ == "__main__":
    # asyncio.run(delete_items(), debug=True)
    # asyncio.run(multi_requests())
    asyncio.run(data_2_del())
