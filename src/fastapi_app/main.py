import subprocess
from pathlib import Path
# TODO: reshape into standard dir
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.fastapi_app.data_base import supabase_client
from .routers import router_consumption, router_task_categories, router_task_entries


def create_app() -> FastAPI:
    # 初始化 FastAPI 和 StrapiClient
    app = FastAPI(
        openapi_prefix="/api",
    )
    # 配置 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许所有源
        allow_credentials=True,
        allow_methods=["*"],  # 允许所有方法
        allow_headers=["*"],  # 允许所有头部
    )

    # Include the routers
    app.include_router(
        router_task_entries,
        prefix="/api/task_entries",
        tags=["task_entries"])
    app.include_router(
        router_task_categories,
        prefix="/api/task_categories",
        tags=["task_categories"])
    app.include_router(
        router_consumption,
        prefix="/api/consumption",
        tags=["consumption"]
    )
    return app


app = create_app()


@app.on_event("startup")
async def set_up():
    # fastapi_scheduler.start()
    await supabase_client.create()


@app.on_event("shutdown")
async def tear_down():
    # fastapi_scheduler.shutdown()
    pass

def server_run(debug: bool = False, port: int = 5000):
    yarn_command = ["yarn", "run", "preview"]
    vue_path = "C:\\Users\\18317\\OneDrive\\vue\\work_space_vue"
    assert Path(vue_path).exists(), "vue_path not exists"
    subprocess.Popen(yarn_command, cwd=vue_path, shell=True)
    if not debug:
        # Run FastAPI with reload

        subprocess.Popen(["uvicorn", "app:app", "--host",
                          "127.0.0.1", "--port", str(port), "--reload"])
    else:

        uvicorn.run(app, port=port)


if __name__ == "__main__":
    server_run(True)
