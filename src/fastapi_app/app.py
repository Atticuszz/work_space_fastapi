import subprocess
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from background_tasks import fastapi_scheduler
from routers import router_consumption, router_task_categories, router_task_entries


def create_app() -> FastAPI:
    # 初始化 FastAPI 和 StrapiClient
    app = FastAPI()
    # 设置 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://localhost:1337",
            "http://localhost:5050", ],
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
    app.include_router(
        router_consumption,
        prefix="/consumption",
        tags=["consumption"]
    )
    return app


app = create_app()


@app.on_event("startup")
async def set_up():
    pass


@app.post("/add_test")
async def add_test(data: dict):
    pass


def server_run(debug: bool = False, port: int = 5000):
    yarn_command = ["yarn", "run", "preview"]
    vue_path = "C:\\Users\\18317\\OneDrive\\vue\\work_space_vue"
    assert Path(vue_path).exists(), "vue_path not exists"
    subprocess.Popen(yarn_command, cwd=vue_path, shell=True)
    fastapi_scheduler.start()

    if not debug:
        # Run FastAPI with reload

        subprocess.Popen(["uvicorn", "app:app", "--host",
                          "127.0.0.1", "--port", str(port), "--reload"])
    else:

        uvicorn.run(app, port=port)


if __name__ == "__main__":
    server_run(True)
