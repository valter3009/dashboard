"""Checklist schemas"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class ChecklistItemBase(BaseModel):
    """Base checklist item schema"""
    content: str = Field(..., min_length=1, max_length=500)


class ChecklistItemCreate(ChecklistItemBase):
    """Schema for creating a checklist item"""
    checklist_id: int
    position: int = 0


class ChecklistItemUpdate(BaseModel):
    """Schema for updating a checklist item"""
    content: Optional[str] = Field(None, min_length=1, max_length=500)
    is_completed: Optional[bool] = None
    position: Optional[int] = None


class ChecklistItem(ChecklistItemBase):
    """Checklist item response schema"""
    id: int
    checklist_id: int
    is_completed: bool
    position: int
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ChecklistBase(BaseModel):
    """Base checklist schema"""
    title: str = Field(..., min_length=1, max_length=255)


class ChecklistCreate(ChecklistBase):
    """Schema for creating a checklist"""
    task_id: int
    position: int = 0


class ChecklistUpdate(BaseModel):
    """Schema for updating a checklist"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    position: Optional[int] = None


class Checklist(ChecklistBase):
    """Checklist response schema"""
    id: int
    task_id: int
    position: int
    created_at: datetime
    items: List[ChecklistItem] = []

    model_config = ConfigDict(from_attributes=True)
