# backend/app/models/clazz.py (班级表，clazz 避免与 Python 关键字 class 冲突)
from sqlalchemy import String, DateTime, Integer, Column, func
from sqlalchemy.orm import relationship

from app.database import Base


class Clazz(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    students = relationship("Student", back_populates="clazz", cascade="all, delete-orphan")
