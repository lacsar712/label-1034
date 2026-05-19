# backend/app/seed.py
import logging
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal, Base
from app.models import Clazz, Student, Course, Grade

logger = logging.getLogger(__name__)


async def run_seed() -> None:
    async with AsyncSessionLocal() as db:
        r = await db.execute(select(Clazz).limit(1))
        if r.scalar_one_or_none() is not None:
            logger.info("seed skipped: data already exists")
            return
        classes = [
            Clazz(name="计算机1班"),
            Clazz(name="计算机2班"),
            Clazz(name="软件1班"),
        ]
        for c in classes:
            db.add(c)
        await db.flush()
        students = [
            Student(name="张三", student_no="2021001", class_id=1),
            Student(name="李四", student_no="2021002", class_id=1),
            Student(name="王五", student_no="2021003", class_id=2),
            Student(name="赵六", student_no="2021004", class_id=2),
            Student(name="钱七", student_no="2021005", class_id=3),
        ]
        for s in students:
            db.add(s)
        await db.flush()
        courses = [
            Course(name="高等数学", credit=Decimal("4.0")),
            Course(name="大学英语", credit=Decimal("3.0")),
            Course(name="程序设计基础", credit=Decimal("4.0")),
            Course(name="数据结构", credit=Decimal("4.0")),
        ]
        for c in courses:
            db.add(c)
        await db.flush()
        grades_data = [
            (1, 1, Decimal("88.5")),
            (1, 2, Decimal("92.0")),
            (1, 3, Decimal("85.0")),
            (2, 1, Decimal("76.0")),
            (2, 2, Decimal("88.5")),
            (2, 3, Decimal("90.0")),
            (3, 1, Decimal("92.0")),
            (3, 2, Decimal("85.0")),
            (3, 4, Decimal("78.5")),
            (4, 1, Decimal("81.0")),
            (4, 3, Decimal("88.0")),
            (4, 4, Decimal("86.0")),
            (5, 2, Decimal("90.0")),
            (5, 3, Decimal("82.5")),
        ]
        for sid, cid, score in grades_data:
            db.add(Grade(student_id=sid, course_id=cid, score=score))
        await db.commit()
        logger.info("seed completed: classes=%s students=%s courses=%s grades=%s",
                    len(classes), len(students), len(courses), len(grades_data))
