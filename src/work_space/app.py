from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.work_space.routers.task_categories import router_task_categories
from src.work_space.routers.task_done_entries import router_task_entries


def create_app() -> FastAPI:
    # 初始化 FastAPI 和 StrapiClient
    app = FastAPI()
    # 设置 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:1337"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include the routers
    app.include_router(
        router_task_entries,
        prefix="/task_entries",
        tags=["task_entries"])
    app.include_router(
        router_task_categories,
        prefix="/task_categories",
        tags=["task_categories"])
    return app


app = create_app()


@app.on_event("startup")
async def set_up():
    pass



@app.post("/add_test")
async def add_test(data: dict):
    pass


if __name__ == "__main__":
    import subprocess

    # 使用subprocess运行uvicorn命令
    subprocess.run(["uvicorn", "app:app", "--host",
                    "127.0.0.1", "--port", "5000", "--reload"])
