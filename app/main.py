import uvicorn

from fastapi import FastAPI

from app.configs.settings import settings
from app.routers.router_1 import router_1

app = FastAPI()
app.include_router(router=router_1, prefix="/router1", tags=["Router 1"])


@app.get("/")
def main_root():
    return {"main": "page"}


if __name__ == '__main__':
    # Вот тут можно будет подключить (или изменить) логи и другие настройки.
    # logger.info("Запуск сервера uvicorn")
    uvicorn.run(
        app="app.main:app",
        reload=settings.RELOAD,
        host=settings.HOST,
        port=settings.PORT,
        log_level="debug"
    )
    # logger.info("Остановка сервера uvicorn")


