"""Time entry schemas"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

from app.schemas.user import User


class TimeEntryBase(BaseModel):
    """Base time entry schema"""
    description: Optional[str] = None


class TimeEntryCreate(TimeEntryBase):
    """Schema for creating a time entry"""
    task_id: int
    started_at: datetime
    ended_at: Optional[datetime] = None


class TimeEntryUpdate(BaseModel):
    """Schema for updating a time entry"""
    description: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None


class TimeEntry(TimeEntryBase):
    """Time entry response schema"""
    id: int
    task_id: int
    user_id: int
    user: Optional[User] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    duration: Optional[int] = None  # in seconds
    is_running: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TimeEntryStart(BaseModel):
    """Schema for starting a timer"""
    task_id: int
    description: Optional[str] = None


class TimeEntryStop(BaseModel):
    """Schema for stopping a timer"""
    time_entry_id: int
