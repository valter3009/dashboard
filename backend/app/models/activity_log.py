"""ActivityLog model"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class ActivityLog(Base):
    """Activity log model for tracking changes"""

    __tablename__ = "activity_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), index=True)
    action = Column(String(100), nullable=False)  # created, updated, deleted, moved, etc.
    entity_type = Column(String(50), nullable=False)  # task, comment, project, etc.
    entity_id = Column(Integer, nullable=False)
    changes = Column(JSONB)  # Store old and new values
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="activity_logs")
    project = relationship("Project", back_populates="activity_logs")

    def __repr__(self):
        return f"<ActivityLog(id={self.id}, action={self.action}, entity_type={self.entity_type})>"
