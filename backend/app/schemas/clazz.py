# backend/app/schemas/clazz.py
from datetime import datetime
from pydantic import BaseModel, Field


class ClazzBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)


class ClazzCreate(ClazzBase):
    pass


class ClazzUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=64)


class ClazzResponse(ClazzBase):
    id: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True
