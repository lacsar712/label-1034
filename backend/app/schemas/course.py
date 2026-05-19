# backend/app/schemas/course.py
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    credit: Decimal = Field(..., ge=0, le=100)


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=128)
    credit: Decimal | None = Field(None, ge=0, le=100)


class CourseResponse(CourseBase):
    id: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True
