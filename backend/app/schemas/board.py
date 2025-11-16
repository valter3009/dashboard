from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# Board schemas
class BoardBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    is_default: int = Field(default=0, ge=0, le=1)  # 0=not default, 1=default


class BoardCreate(BoardBase):
    project_id: int


class BoardUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    is_default: Optional[int] = Field(None, ge=0, le=1)


class Board(BoardBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Column schemas
class ColumnBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    position: int = Field(ge=0)
    wip_limit: Optional[int] = Field(None, ge=0)


class ColumnCreate(ColumnBase):
    board_id: int


class ColumnUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    position: Optional[int] = Field(None, ge=0)
    wip_limit: Optional[int] = Field(None, ge=0)


class Column(ColumnBase):
    id: int
    board_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Board with columns
class BoardWithColumns(Board):
    columns: list[Column] = []
