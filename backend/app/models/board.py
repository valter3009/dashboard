"""Board and Column models for Kanban"""

from sqlalchemy import Column as SQLColumn, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Board(Base):
    """Kanban board model"""

    __tablename__ = "boards"

    id = SQLColumn(Integer, primary_key=True, index=True)
    project_id = SQLColumn(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = SQLColumn(String(255), nullable=False)
    description = SQLColumn(Text)
    is_default = SQLColumn(Integer, default=0)  # Boolean: 1=default, 0=not default
    position = SQLColumn(Integer, default=0)
    created_at = SQLColumn(DateTime(timezone=True), server_default=func.now())
    updated_at = SQLColumn(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="boards")
    columns = relationship("Column", back_populates="board", cascade="all, delete-orphan", order_by="Column.position")
    tasks = relationship("Task", back_populates="board", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Board(id={self.id}, name={self.name})>"


class Column(Base):
    """Kanban column model"""

    __tablename__ = "columns"

    id = SQLColumn(Integer, primary_key=True, index=True)
    board_id = SQLColumn(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
    name = SQLColumn(String(100), nullable=False)
    position = SQLColumn(Integer, nullable=False)
    wip_limit = SQLColumn(Integer)  # Work In Progress limit
    created_at = SQLColumn(DateTime(timezone=True), server_default=func.now())
    updated_at = SQLColumn(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    board = relationship("Board", back_populates="columns")
    tasks = relationship("Task", back_populates="column")

    def __repr__(self):
        return f"<Column(id={self.id}, name={self.name}, position={self.position})>"
