"""Comment schemas"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

from app.schemas.user import User


class CommentBase(BaseModel):
    """Base comment schema"""
    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    """Schema for creating a comment"""
    task_id: int
    parent_comment_id: Optional[int] = None


class CommentUpdate(BaseModel):
    """Schema for updating a comment"""
    content: str = Field(..., min_length=1)


class Comment(CommentBase):
    """Comment response schema"""
    id: int
    task_id: int
    user_id: int
    user: Optional[User] = None
    parent_comment_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    replies: List["Comment"] = []

    model_config = ConfigDict(from_attributes=True)
