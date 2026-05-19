# backend/app/main.py
import asyncio
import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.models import Clazz, Student, Course, Grade  # 显式导入，确保表注册到 Base.metadata
from app.api import students, courses, grades, classes
from app.seed import run_seed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


async def _init_db() -> None:
    """在 Python 中初始化数据库：创建所有表。"""
    for i in range(30):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("database tables created successfully")
            return
        except Exception as e:
            logger.warning("db init attempt %s failed: %s", i + 1, e)
            await asyncio.sleep(2)
    raise RuntimeError("database init failed after 30 retries")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await _init_db()
    await run_seed()
    yield
    await engine.dispose()


app = FastAPI(
    title="学生成绩管理系统 API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(courses.router)
app.include_router(grades.router)
app.include_router(classes.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
