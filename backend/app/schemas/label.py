"""Label schemas"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class LabelBase(BaseModel):
    """Base label schema"""
    name: str = Field(..., min_length=1, max_length=100)
    color: str = Field(..., pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")


class LabelCreate(LabelBase):
    """Schema for creating a label"""
    project_id: int


class LabelUpdate(BaseModel):
    """Schema for updating a label"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = Field(None, pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")


class Label(LabelBase):
    """Label response schema"""
    id: int
    project_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
