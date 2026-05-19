# backend/app/api/courses.py
import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import Course
from app.schemas import CourseCreate, CourseUpdate, CourseResponse

router = APIRouter(prefix="/courses", tags=["courses"])
logger = logging.getLogger(__name__)


@router.get("", response_model=list[CourseResponse])
async def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    q = select(Course).order_by(Course.id).offset(skip).limit(limit)
    result = await db.execute(q)
    return list(result.scalars().all())


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.get(Course, course_id)
    if not r:
        raise HTTPException(status_code=404, detail="课程不存在")
    return r


@router.post("", response_model=CourseResponse, status_code=201)
async def create_course(data: CourseCreate, db: AsyncSession = Depends(get_db)):
    obj = Course(**data.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    logger.info("created course id=%s name=%s", obj.id, obj.name)
    return obj


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int, data: CourseUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await db.get(Course, course_id)
    if not obj:
        raise HTTPException(status_code=404, detail="课程不存在")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.flush()
    await db.refresh(obj)
    logger.info("updated course id=%s", course_id)
    return obj


@router.delete("/{course_id}", status_code=204)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Course, course_id)
    if not obj:
        raise HTTPException(status_code=404, detail="课程不存在")
    await db.delete(obj)
    await db.flush()
    logger.info("deleted course id=%s", course_id)
