"""Project and ProjectMember models"""

from sqlalchemy import Column, Integer, String, Text, Date, Numeric, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Project(Base):
    """Project model"""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    key = Column(String(10), nullable=False)  # Short project code (PROJ, DEV, etc.)
    description = Column(Text)
    status = Column(String(50), default="active")  # active, archived, on_hold
    start_date = Column(Date)
    end_date = Column(Date)
    budget = Column(Numeric(15, 2))
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Unique constraint
    __table_args__ = (UniqueConstraint("organization_id", "key", name="uix_org_project_key"),)

    # Relationships
    organization = relationship("Organization", back_populates="projects")
    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
    boards = relationship("Board", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    labels = relationship("Label", back_populates="project", cascade="all, delete-orphan")
    custom_fields = relationship("CustomField", back_populates="project", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="project")

    def __repr__(self):
        return f"<Project(id={self.id}, key={self.key}, name={self.name})>"


class ProjectMember(Base):
    """Project membership model with roles"""

    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(50), nullable=False)  # manager, developer, viewer
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    # Unique constraint
    __table_args__ = (UniqueConstraint("project_id", "user_id", name="uix_project_user"),)

    # Relationships
    project = relationship("Project", back_populates="members")
    user = relationship("User", back_populates="project_memberships")

    def __repr__(self):
        return f"<ProjectMember(project_id={self.project_id}, user_id={self.user_id}, role={self.role})>"
