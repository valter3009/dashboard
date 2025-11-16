"""Board and Column schemas"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class BoardBase(BaseModel):
    """Base board schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class BoardCreate(BoardBase):
    """Schema for creating a board"""
    project_id: int
    position: int = 0


class BoardUpdate(BaseModel):
    """Schema for updating a board"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    position: Optional[int] = None


class Board(BoardBase):
    """Board response schema"""
    id: int
    project_id: int
    position: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ColumnBase(BaseModel):
    """Base column schema"""
    name: str = Field(..., min_length=1, max_length=100)
    position: int


class ColumnCreate(ColumnBase):
    """Schema for creating a column"""
    board_id: int
    wip_limit: Optional[int] = None


class ColumnUpdate(BaseModel):
    """Schema for updating a column"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    position: Optional[int] = None
    wip_limit: Optional[int] = None


class Column(ColumnBase):
    """Column response schema"""
    id: int
    board_id: int
    wip_limit: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BoardWithColumns(Board):
    """Board with columns list"""
    columns: List[Column] = []

    model_config = ConfigDict(from_attributes=True)
