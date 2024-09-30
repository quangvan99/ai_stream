from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import managers, tasks, cameras, fakedata
from database import db, client


# Sự kiện khởi động và tắt ứng dụng
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    client.close()

app = FastAPI(lifespan=lifespan)

# Register router
app.include_router(managers.router)
app.include_router(tasks.router)
app.include_router(cameras.router)
app.include_router(fakedata.router)