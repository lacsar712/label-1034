# backend/app/models/course.py
from sqlalchemy import String, Numeric, DateTime, Integer, Column, func
from sqlalchemy.orm import relationship

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False, index=True)
    credit = Column(Numeric(3, 1), nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    grades = relationship("Grade", back_populates="course", cascade="all, delete-orphan")
