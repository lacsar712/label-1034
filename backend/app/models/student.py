# backend/app/models/student.py
from sqlalchemy import String, DateTime, Integer, Column, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, index=True)
    student_no = Column(String(32), unique=True, nullable=False, index=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="RESTRICT"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    clazz = relationship("Clazz", back_populates="students")
    grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")
