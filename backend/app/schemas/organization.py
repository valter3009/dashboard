"""Organization schemas"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

from app.schemas.user import User
from app.utils.constants import UserRole


class OrganizationBase(BaseModel):
    """Base organization schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    """Schema for creating an organization"""
    pass


class OrganizationUpdate(BaseModel):
    """Schema for updating an organization"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    logo_url: Optional[str] = None


class Organization(OrganizationBase):
    """Organization response schema"""
    id: int
    logo_url: Optional[str] = None
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrganizationMemberBase(BaseModel):
    """Base organization member schema"""
    role: UserRole


class OrganizationMemberCreate(OrganizationMemberBase):
    """Schema for adding a member to organization"""
    user_id: int


class OrganizationMember(OrganizationMemberBase):
    """Organization member response schema"""
    id: int
    organization_id: int
    user_id: int
    user: Optional[User] = None
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrganizationWithMembers(Organization):
    """Organization with members list"""
    members: List[OrganizationMember] = []

    model_config = ConfigDict(from_attributes=True)
