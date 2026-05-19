# backend/app/schemas/__init__.py
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.schemas.grade import GradeCreate, GradeUpdate, GradeResponse, GradeDetail

__all__ = [
    "StudentCreate", "StudentUpdate", "StudentResponse",
    "CourseCreate", "CourseUpdate", "CourseResponse",
    "GradeCreate", "GradeUpdate", "GradeResponse", "GradeDetail",
]
