"""Label and TaskLabel models"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Label(Base):
    """Label/Tag model for tasks"""

    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    color = Column(String(7), nullable=False)  # HEX color code
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Unique constraint
    __table_args__ = (UniqueConstraint("project_id", "name", name="uix_project_label"),)

    # Relationships
    project = relationship("Project", back_populates="labels")
    task_labels = relationship("TaskLabel", back_populates="label", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Label(id={self.id}, name={self.name}, color={self.color})>"


class TaskLabel(Base):
    """Many-to-many relationship between tasks and labels"""

    __tablename__ = "task_labels"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    label_id = Column(Integer, ForeignKey("labels.id", ondelete="CASCADE"), nullable=False)

    # Unique constraint
    __table_args__ = (UniqueConstraint("task_id", "label_id", name="uix_task_label"),)

    # Relationships
    task = relationship("Task", back_populates="labels")
    label = relationship("Label", back_populates="task_labels")

    def __repr__(self):
        return f"<TaskLabel(task_id={self.task_id}, label_id={self.label_id})>"
