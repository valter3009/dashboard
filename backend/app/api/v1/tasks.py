"""Task API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

from ...database import get_db
from ...models.user import User as UserModel
from ...models.task import Task as TaskModel, TaskAssignee
from ...models.project import Project as ProjectModel, ProjectMember
from ...models.board import Board as BoardModel, Column as ColumnModel
from ...schemas.task import (
    Task,
    TaskCreate,
    TaskUpdate,
    TaskMove,
    TaskAssigneeCreate,
    TaskWithDetails,
)
from ...dependencies import get_current_user

router = APIRouter()


def check_project_access(project_id: int, user: UserModel, db: Session) -> ProjectModel:
    """Check if user has access to project"""
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    is_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user.id
    ).first()

    if not is_member:
        raise HTTPException(status_code=403, detail="Access denied")

    return project


def check_task_access(task_id: int, user: UserModel, db: Session) -> TaskModel:
    """Check if user has access to task"""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    check_project_access(task.project_id, user, db)
    return task


def get_next_task_number(project_id: int, db: Session) -> int:
    """Get next task number for project"""
    max_task = db.query(TaskModel).filter(
        TaskModel.project_id == project_id
    ).order_by(TaskModel.task_number.desc()).first()

    return (max_task.task_number + 1) if max_task else 1


@router.get("/", response_model=List[Task])
def get_tasks(
    project_id: Optional[int] = Query(None),
    board_id: Optional[int] = Query(None),
    column_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Get tasks with filters"""
    query = db.query(TaskModel)

    if project_id:
        check_project_access(project_id, current_user, db)
        query = query.filter(TaskModel.project_id == project_id)

    if board_id:
        query = query.filter(TaskModel.board_id == board_id)

    if column_id:
        query = query.filter(TaskModel.column_id == column_id)

    tasks = query.order_by(TaskModel.position, TaskModel.created_at.desc()).all()
    return tasks


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Create a new task"""
    check_project_access(task_data.project_id, current_user, db)

    # Verify board exists
    board = db.query(BoardModel).filter(
        BoardModel.id == task_data.board_id,
        BoardModel.project_id == task_data.project_id
    ).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    # Verify column if provided
    if task_data.column_id:
        column = db.query(ColumnModel).filter(
            ColumnModel.id == task_data.column_id,
            ColumnModel.board_id == task_data.board_id
        ).first()
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

    # Get next task number
    task_number = get_next_task_number(task_data.project_id, db)

    # Get max position in column
    max_position = 0
    if task_data.column_id:
        max_task = db.query(TaskModel).filter(
            TaskModel.column_id == task_data.column_id
        ).order_by(TaskModel.position.desc()).first()
        max_position = (max_task.position + 1) if max_task else 0

    # Create task
    db_task = TaskModel(
        project_id=task_data.project_id,
        board_id=task_data.board_id,
        column_id=task_data.column_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        type=task_data.type,
        story_points=task_data.story_points,
        estimated_hours=task_data.estimated_hours,
        start_date=task_data.start_date,
        due_date=task_data.due_date,
        parent_task_id=task_data.parent_task_id,
        task_number=task_number,
        position=max_position,
        creator_id=current_user.id,
        actual_hours=Decimal(0),
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # Assign users if provided
    if hasattr(task_data, 'assignee_ids') and task_data.assignee_ids:
        for user_id in task_data.assignee_ids:
            assignee = TaskAssignee(task_id=db_task.id, user_id=user_id)
            db.add(assignee)
        db.commit()
        db.refresh(db_task)

    return db_task


@router.patch("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Update task"""
    task = check_task_access(task_id, current_user, db)

    update_data = task_data.model_dump(exclude_unset=True)

    # If moving to different column, update position
    if 'column_id' in update_data and update_data['column_id'] != task.column_id:
        column = db.query(ColumnModel).filter(
            ColumnModel.id == update_data['column_id'],
            ColumnModel.board_id == task.board_id
        ).first()
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        max_task = db.query(TaskModel).filter(
            TaskModel.column_id == update_data['column_id']
        ).order_by(TaskModel.position.desc()).first()
        update_data['position'] = (max_task.position + 1) if max_task else 0

    # Update completed_at if status changed to done
    if 'status' in update_data and update_data['status'] == 'done' and task.status != 'done':
        task.completed_at = datetime.utcnow()

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Delete task"""
    task = check_task_access(task_id, current_user, db)
    db.delete(task)
    db.commit()
    return None
