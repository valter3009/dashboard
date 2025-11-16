"""Project schemas"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal

from app.schemas.user import User
from app.utils.constants import ProjectStatus, ProjectRole


class ProjectBase(BaseModel):
    """Base project schema"""
    name: str = Field(..., min_length=1, max_length=255)
    key: str = Field(..., min_length=2, max_length=10, pattern="^[A-Z][A-Z0-9]*$")
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[Decimal] = None


class ProjectCreate(ProjectBase):
    """Schema for creating a project"""
    organization_id: int


class ProjectUpdate(BaseModel):
    """Schema for updating a project"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[Decimal] = None


class Project(ProjectBase):
    """Project response schema"""
    id: int
    organization_id: int
    status: ProjectStatus
    owner_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectMemberBase(BaseModel):
    """Base project member schema"""
    role: ProjectRole


class ProjectMemberCreate(ProjectMemberBase):
    """Schema for adding a member to project"""
    user_id: int


class ProjectMember(ProjectMemberBase):
    """Project member response schema"""
    id: int
    project_id: int
    user_id: int
    user: Optional[User] = None
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectWithMembers(Project):
    """Project with members list"""
    members: List[ProjectMember] = []

    model_config = ConfigDict(from_attributes=True)
