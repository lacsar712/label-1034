# backend/app/schemas/student.py
from datetime import datetime
from pydantic import BaseModel, Field


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    student_no: str = Field(..., min_length=1, max_length=32)
    class_id: int = Field(..., gt=0)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=64)
    student_no: str | None = Field(None, min_length=1, max_length=32)
    class_id: int | None = Field(None, gt=0)


class StudentResponse(BaseModel):
    id: int
    name: str
    student_no: str
    class_id: int
    class_name: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True
