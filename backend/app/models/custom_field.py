"""CustomField and TaskCustomFieldValue models"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class CustomField(Base):
    """Custom field model for projects"""

    __tablename__ = "custom_fields"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    field_type = Column(String(50), nullable=False)  # text, number, date, select, multi_select
    options = Column(JSONB)  # For select types
    is_required = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    project = relationship("Project", back_populates="custom_fields")
    task_values = relationship("TaskCustomFieldValue", back_populates="custom_field", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CustomField(id={self.id}, name={self.name}, type={self.field_type})>"


class TaskCustomFieldValue(Base):
    """Task custom field value model"""

    __tablename__ = "task_custom_field_values"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    custom_field_id = Column(Integer, ForeignKey("custom_fields.id", ondelete="CASCADE"), nullable=False)
    value = Column(Text)

    # Unique constraint
    __table_args__ = (UniqueConstraint("task_id", "custom_field_id", name="uix_task_custom_field"),)

    # Relationships
    task = relationship("Task", back_populates="custom_field_values")
    custom_field = relationship("CustomField", back_populates="task_values")

    def __repr__(self):
        return f"<TaskCustomFieldValue(task_id={self.task_id}, field_id={self.custom_field_id})>"
