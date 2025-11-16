"""Task schemas"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

from app.schemas.user import User
from app.schemas.label import Label
from app.utils.constants import TaskPriority, TaskStatus, TaskType, DependencyType


class TaskBase(BaseModel):
    """Base task schema"""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    type: TaskType = TaskType.TASK
    story_points: Optional[int] = None
    estimated_hours: Optional[Decimal] = None


class TaskCreate(TaskBase):
    """Schema for creating a task"""
    project_id: int
    board_id: int
    column_id: Optional[int] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    parent_task_id: Optional[int] = None
    assignee_ids: List[int] = []


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    type: Optional[TaskType] = None
    story_points: Optional[int] = None
    estimated_hours: Optional[Decimal] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    column_id: Optional[int] = None
    position: Optional[int] = None


class TaskMove(BaseModel):
    """Schema for moving a task"""
    column_id: int
    position: int


class TaskAssigneeCreate(BaseModel):
    """Schema for assigning a user to task"""
    user_id: int


class TaskDependencyCreate(BaseModel):
    """Schema for creating task dependency"""
    depends_on_task_id: int
    dependency_type: DependencyType = DependencyType.FINISH_TO_START


class Task(TaskBase):
    """Task response schema"""
    id: int
    project_id: int
    board_id: int
    column_id: Optional[int] = None
    task_number: int
    status: TaskStatus
    actual_hours: Decimal
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    position: int
    creator_id: Optional[int] = None
    parent_task_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    # Related data (optional, can be populated)
    creator: Optional[User] = None
    assignees: List[User] = []
    labels: List[Label] = []

    model_config = ConfigDict(from_attributes=True)


class TaskWithDetails(Task):
    """Task with all related details"""
    comments_count: int = 0
    attachments_count: int = 0
    checklists_count: int = 0
    time_tracked: Decimal = Decimal(0)

    model_config = ConfigDict(from_attributes=True)
