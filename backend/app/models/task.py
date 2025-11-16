"""Task and related models"""

from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Task(Base):
    """Task model"""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False, index=True)
    column_id = Column(Integer, ForeignKey("columns.id", ondelete="SET NULL"), index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    task_number = Column(Integer, nullable=False)  # Auto-increment per project (PROJ-1, PROJ-2)
    priority = Column(String(50), default="medium")  # low, medium, high, critical
    status = Column(String(50), default="new")  # new, active, on_hold, done
    type = Column(String(50), default="task")  # task, bug, feature, epic
    story_points = Column(Integer)
    estimated_hours = Column(Numeric(10, 2))
    actual_hours = Column(Numeric(10, 2), default=0)
    start_date = Column(DateTime(timezone=True))
    due_date = Column(DateTime(timezone=True), index=True)
    completed_at = Column(DateTime(timezone=True))
    position = Column(Integer, default=0)  # Position in column
    creator_id = Column(Integer, ForeignKey("users.id"), index=True)
    parent_task_id = Column(Integer, ForeignKey("tasks.id"))  # For subtasks
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="tasks")
    board = relationship("Board", back_populates="tasks")
    column = relationship("Column", back_populates="tasks")
    creator = relationship("User", foreign_keys=[creator_id], back_populates="created_tasks")
    assignees = relationship("TaskAssignee", back_populates="task", cascade="all, delete-orphan")
    labels = relationship("TaskLabel", back_populates="task", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="task", cascade="all, delete-orphan")
    checklists = relationship("Checklist", back_populates="task", cascade="all, delete-orphan")
    time_entries = relationship("TimeEntry", back_populates="task", cascade="all, delete-orphan")
    custom_field_values = relationship("TaskCustomFieldValue", back_populates="task", cascade="all, delete-orphan")

    # Dependencies
    dependencies = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.task_id",
        back_populates="task",
        cascade="all, delete-orphan"
    )
    dependent_tasks = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.depends_on_task_id",
        back_populates="depends_on_task",
        cascade="all, delete-orphan"
    )

    # Subtasks
    parent_task = relationship("Task", remote_side=[id], backref="subtasks")

    @property
    def task_key(self) -> str:
        """Get task key (e.g., PROJ-123)"""
        # This will be populated from project.key in the application logic
        return f"TASK-{self.task_number}"

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, number={self.task_number})>"


class TaskAssignee(Base):
    """Task assignee model for multiple assignees"""

    __tablename__ = "task_assignees"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

    # Unique constraint
    __table_args__ = (UniqueConstraint("task_id", "user_id", name="uix_task_user"),)

    # Relationships
    task = relationship("Task", back_populates="assignees")
    user = relationship("User", back_populates="assigned_tasks")

    def __repr__(self):
        return f"<TaskAssignee(task_id={self.task_id}, user_id={self.user_id})>"


class TaskDependency(Base):
    """Task dependency model for Gantt chart"""

    __tablename__ = "task_dependencies"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    depends_on_task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    dependency_type = Column(String(50), default="finish_to_start")
    # finish_to_start, start_to_start, finish_to_finish, start_to_finish
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Unique constraint
    __table_args__ = (UniqueConstraint("task_id", "depends_on_task_id", name="uix_task_dependency"),)

    # Relationships
    task = relationship("Task", foreign_keys=[task_id], back_populates="dependencies")
    depends_on_task = relationship("Task", foreign_keys=[depends_on_task_id], back_populates="dependent_tasks")

    def __repr__(self):
        return f"<TaskDependency(task_id={self.task_id}, depends_on={self.depends_on_task_id})>"
