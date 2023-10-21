import asyncio
import pprint
import timeit

from src.fastapi_app.data_base.client import SupaBase

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


async def init_new_filed():
    data = await supabase_client.get_table("task_done_list")
    # 根据detail字段分割成可以选择的内容，-1表示自己输入，-2表示不需要输入
    # 将选择的内容追加进item的target字段，并且收集到收集表中
    new_target = set()
    for item in data:
        if item.get('detail', None):
            # 根据‘/n',' ' ,','分割
            options = item['detail'].split('\n')
            for i in range(len(options)):
                print(i, ':', options[i])
            op = input("请输入选项序号：")
            if int(op) >= 0:
                item['target'].append(options[int(op)])
                new_target.add(options[int(op)])
            elif op == '-1':
                u_input = input("input your ：")
                item['target'].append(u_input)
                new_target.add(u_input)

    # update task_done_list

    # undate single_page


async def transform2():
    data = await supabase_client.get_table("task_done_list")

    # data transform
    data_map = {
        'category': 'categories',
        'task': 'tasks',
        'location': 'locations'}
    for item in data:
        for key in data_map:
            if isinstance(item[key], str):
                item[key] = item[key].split(',')
            item[data_map[key]] = item[key]
    pprint.pprint(data)
    result = await multi_requests(data, "upsert")


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


async def multi_requests(data: list, options: str):
    # with open("test_data.json", "r") as f:
    #     data = json.load(f)
    chunk_size = 4000
    for i in range(0, len(data), chunk_size):
        chunk_data = data[i:i + chunk_size]
        match options:
            case "upsert":
                tasks = [asyncio.ensure_future(safe_upsert(item))
                         for item in chunk_data]
            case 'delete':
                tasks = [
                    asyncio.ensure_future(
                        safe_delete(
                            item["uuid"])) for item in chunk_data]
            case _:
                raise ValueError("options must be 'upsert' or 'delete'")
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


def main(func: callable, *args, **kwargs):
    asyncio.run(func(*args, **kwargs))


if __name__ == "__main__":
    main(init_new_filed)
