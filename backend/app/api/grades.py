# backend/app/api/grades.py
import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Grade, Student, Course
from app.schemas import GradeCreate, GradeUpdate, GradeResponse, GradeDetail

router = APIRouter(prefix="/grades", tags=["grades"])
logger = logging.getLogger(__name__)


@router.get("", response_model=list[GradeDetail])
async def list_grades(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    student_id: int | None = Query(None),
    course_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    q = (
        select(Grade)
        .options(selectinload(Grade.student), selectinload(Grade.course))
        .order_by(Grade.id)
    )
    if student_id is not None:
        q = q.where(Grade.student_id == student_id)
    if course_id is not None:
        q = q.where(Grade.course_id == course_id)
    q = q.offset(skip).limit(limit)
    result = await db.execute(q)
    rows = result.scalars().unique().all()
    out = []
    for g in rows:
        out.append(
            GradeDetail(
                id=g.id,
                student_id=g.student_id,
                course_id=g.course_id,
                score=g.score,
                exam_date=g.exam_date,
                created_at=g.created_at,
                student_name=g.student.name if g.student else None,
                student_no=g.student.student_no if g.student else None,
                course_name=g.course.name if g.course else None,
                course_credit=g.course.credit if g.course else None,
            )
        )
    return out


@router.get("/{grade_id}", response_model=GradeDetail)
async def get_grade(grade_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(
        select(Grade)
        .options(selectinload(Grade.student), selectinload(Grade.course))
        .where(Grade.id == grade_id)
    )
    g = r.scalar_one_or_none()
    if not g:
        raise HTTPException(status_code=404, detail="成绩记录不存在")
    return GradeDetail(
        id=g.id,
        student_id=g.student_id,
        course_id=g.course_id,
        score=g.score,
        exam_date=g.exam_date,
        created_at=g.created_at,
        student_name=g.student.name if g.student else None,
        student_no=g.student.student_no if g.student else None,
        course_name=g.course.name if g.course else None,
        course_credit=g.course.credit if g.course else None,
    )


@router.post("", response_model=GradeResponse, status_code=201)
async def create_grade(data: GradeCreate, db: AsyncSession = Depends(get_db)):
    student = await db.get(Student, data.student_id)
    if not student:
        raise HTTPException(status_code=400, detail="学生不存在")
    course = await db.get(Course, data.course_id)
    if not course:
        raise HTTPException(status_code=400, detail="课程不存在")
    r = await db.execute(
        select(Grade).where(
            Grade.student_id == data.student_id, Grade.course_id == data.course_id
        )
    )
    if r.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="该学生该课程已有成绩记录")
    obj = Grade(**data.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    logger.info("created grade id=%s student=%s course=%s", obj.id, data.student_id, data.course_id)
    return obj


@router.put("/{grade_id}", response_model=GradeResponse)
async def update_grade(
    grade_id: int, data: GradeUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await db.get(Grade, grade_id)
    if not obj:
        raise HTTPException(status_code=404, detail="成绩记录不存在")
    obj.score = data.score
    await db.flush()
    await db.refresh(obj)
    logger.info("updated grade id=%s", grade_id)
    return obj


@router.delete("/{grade_id}", status_code=204)
async def delete_grade(grade_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Grade, grade_id)
    if not obj:
        raise HTTPException(status_code=404, detail="成绩记录不存在")
    await db.delete(obj)
    await db.flush()
    logger.info("deleted grade id=%s", grade_id)
