# backend/app/api/classes.py
import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import Clazz
from app.schemas.clazz import ClazzCreate, ClazzUpdate, ClazzResponse

router = APIRouter(prefix="/classes", tags=["classes"])
logger = logging.getLogger(__name__)


@router.get("", response_model=list[ClazzResponse])
async def list_classes(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    q = select(Clazz).order_by(Clazz.id).offset(skip).limit(limit)
    result = await db.execute(q)
    return list(result.scalars().all())


@router.get("/{class_id}", response_model=ClazzResponse)
async def get_class(class_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.get(Clazz, class_id)
    if not r:
        raise HTTPException(status_code=404, detail="班级不存在")
    return r


@router.post("", response_model=ClazzResponse, status_code=201)
async def create_class(data: ClazzCreate, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Clazz).where(Clazz.name == data.name))
    if r.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="班级名称已存在")
    obj = Clazz(**data.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    logger.info("created class id=%s name=%s", obj.id, obj.name)
    return obj


@router.put("/{class_id}", response_model=ClazzResponse)
async def update_class(
    class_id: int, data: ClazzUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await db.get(Clazz, class_id)
    if not obj:
        raise HTTPException(status_code=404, detail="班级不存在")
    if data.name is not None:
        r = await db.execute(select(Clazz).where(Clazz.name == data.name).where(Clazz.id != class_id))
        if r.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="班级名称已存在")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.flush()
    await db.refresh(obj)
    logger.info("updated class id=%s", class_id)
    return obj


@router.delete("/{class_id}", status_code=204)
async def delete_class(class_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Clazz, class_id)
    if not obj:
        raise HTTPException(status_code=404, detail="班级不存在")
    from app.models import Student
    r = await db.execute(select(Student).where(Student.class_id == class_id).limit(1))
    if r.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="该班级下还有学生，无法删除")
    await db.delete(obj)
    await db.flush()
    logger.info("deleted class id=%s", class_id)
