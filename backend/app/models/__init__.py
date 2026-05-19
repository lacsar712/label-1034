# backend/app/models/__init__.py
from app.models.clazz import Clazz
from app.models.student import Student
from app.models.course import Course
from app.models.grade import Grade

__all__ = ["Clazz", "Student", "Course", "Grade"]
