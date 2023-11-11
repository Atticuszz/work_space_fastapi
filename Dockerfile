# 第一阶段：使用 Poetry 导出 requirements.txt
FROM python:3.11-rc-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY poetry.lock pyproject.toml /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# 第二阶段：构建最终镜像
FROM python:3.11-rc-slim

WORKDIR /app

# 仅复制 requirements.txt 并安装依赖
COPY --from=requirements-stage /tmp/requirements.txt /app/

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 复制整个项目到容器中
COPY . /app

# 设置环境变量
ENV PORT=5000

# 暴露端口
EXPOSE 5000

# 运行 FastAPI 应用
CMD ["uvicorn", "src.fastapi_app.main:app", "--host", "0.0.0.0", "--port", "5000"]
