# backend/app/api/students.py
import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Student
from app.schemas import StudentCreate, StudentUpdate, StudentResponse

router = APIRouter(prefix="/students", tags=["students"])
logger = logging.getLogger(__name__)


def _student_to_response(s) -> StudentResponse:
    return StudentResponse(
        id=s.id,
        name=s.name,
        student_no=s.student_no,
        class_id=s.class_id,
        class_name=s.clazz.name if s.clazz else None,
        created_at=s.created_at,
    )


@router.get("", response_model=list[StudentResponse])
async def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    class_id: int | None = Query(None, description="按班级ID筛选"),
    db: AsyncSession = Depends(get_db),
):
    q = select(Student).options(selectinload(Student.clazz)).order_by(Student.id)
    if class_id is not None:
        q = q.where(Student.class_id == class_id)
    q = q.offset(skip).limit(limit)
    result = await db.execute(q)
    rows = result.scalars().unique().all()
    return [_student_to_response(s) for s in rows]


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Student).options(selectinload(Student.clazz)).where(Student.id == student_id))
    s = r.scalar_one_or_none()
    if not s:
        raise HTTPException(status_code=404, detail="学生不存在")
    return _student_to_response(s)


@router.post("", response_model=StudentResponse, status_code=201)
async def create_student(data: StudentCreate, db: AsyncSession = Depends(get_db)):
    from app.models import Clazz
    if await db.get(Clazz, data.class_id) is None:
        raise HTTPException(status_code=400, detail="班级不存在")
    r = await db.execute(select(Student).where(Student.student_no == data.student_no))
    if r.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="学号已存在")
    obj = Student(**data.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    await db.refresh(obj, ["clazz"])
    logger.info("created student id=%s student_no=%s", obj.id, obj.student_no)
    return _student_to_response(obj)


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int, data: StudentUpdate, db: AsyncSession = Depends(get_db)
):
    from app.models import Clazz
    obj = await db.get(Student, student_id)
    if not obj:
        raise HTTPException(status_code=404, detail="学生不存在")
    if data.class_id is not None and await db.get(Clazz, data.class_id) is None:
        raise HTTPException(status_code=400, detail="班级不存在")
    if data.student_no is not None:
        r = await db.execute(select(Student).where(Student.student_no == data.student_no, Student.id != student_id))
        if r.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="学号已存在")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.flush()
    await db.refresh(obj)
    await db.refresh(obj, ["clazz"])
    logger.info("updated student id=%s", student_id)
    return _student_to_response(obj)


@router.delete("/{student_id}", status_code=204)
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Student, student_id)
    if not obj:
        raise HTTPException(status_code=404, detail="学生不存在")
    await db.delete(obj)
    await db.flush()
    logger.info("deleted student id=%s", student_id)
