# backend/app/schemas/grade.py
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class GradeBase(BaseModel):
    student_id: int
    course_id: int
    score: Decimal = Field(..., ge=0, le=100)


class GradeCreate(GradeBase):
    pass


class GradeUpdate(BaseModel):
    score: Decimal = Field(..., ge=0, le=100)


class GradeResponse(GradeBase):
    id: int
    exam_date: datetime | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class GradeDetail(GradeResponse):
    student_name: str | None = None
    student_no: str | None = None
    course_name: str | None = None
    course_credit: Decimal | None = None
