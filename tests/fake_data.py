import json
import uuid
from datetime import datetime

from faker import Faker

# 初始化 Faker 实例
fake = Faker()


# 定义生成单条数据的函数


def generate_single_data():
    return {
        'id': fake.random_int(min=1, max=10000),  # 随机生成ID
        'slot': fake.time(pattern="%H:%M", end_datetime=None),  # 随机生成时间段
        'detail': fake.word(),  # 随机生成任务详情
        'task': [fake.word() for _ in range(1, 4)],  # 随机生成任务列表
        'category': [fake.word() for _ in range(1, 3)],  # 随机生成分类列表
        'location': fake.city(),  # 随机生成地点
        'uuid': str(uuid.uuid4()),  # 生成唯一的 UUID
        # 随机生成日期
        'date': fake.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d'),
        'createdAt': datetime.utcnow().isoformat() + 'Z',  # 创建时间
        'updatedAt': datetime.utcnow().isoformat() + 'Z'  # 更新时间
    }


# 定义生成多条数据的函数


def generate_multiple_data(n):
    data = [generate_single_data() for _ in range(n)]
    # 将数据保存为 JSON 文件
    with open('test_data.json', 'w') as f:
        json.dump(data, f)

    print("生成的 JSON 文件已保存为 test_data.json")
    return


if __name__ == "__main__":
    # 生成 1000 条测试数据
    generate_multiple_data(100000)
