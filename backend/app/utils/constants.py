"""Application constants and enums"""

from enum import Enum


class UserRole(str, Enum):
    """User roles in organization"""
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class ProjectRole(str, Enum):
    """User roles in project"""
    MANAGER = "manager"
    DEVELOPER = "developer"
    VIEWER = "viewer"


class TaskPriority(str, Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(str, Enum):
    """Task status"""
    NEW = "new"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    DONE = "done"


class TaskType(str, Enum):
    """Task types"""
    TASK = "task"
    BUG = "bug"
    FEATURE = "feature"
    EPIC = "epic"


class ProjectStatus(str, Enum):
    """Project status"""
    ACTIVE = "active"
    ARCHIVED = "archived"
    ON_HOLD = "on_hold"


class DependencyType(str, Enum):
    """Task dependency types for Gantt chart"""
    FINISH_TO_START = "finish_to_start"
    START_TO_START = "start_to_start"
    FINISH_TO_FINISH = "finish_to_finish"
    START_TO_FINISH = "start_to_finish"


class NotificationType(str, Enum):
    """Notification types"""
    TASK_ASSIGNED = "task_assigned"
    TASK_UPDATED = "task_updated"
    TASK_COMMENTED = "task_commented"
    TASK_MENTIONED = "task_mentioned"
    PROJECT_INVITATION = "project_invitation"
    DEADLINE_APPROACHING = "deadline_approaching"
