from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...database import get_db
from ...models.user import User as UserModel
from ...models.board import Board as BoardModel, Column as ColumnModel
from ...models.project import Project as ProjectModel, ProjectMember
from ...schemas.board import (
    Board,
    BoardCreate,
    BoardUpdate,
    BoardWithColumns,
    Column,
    ColumnCreate,
    ColumnUpdate,
)
from ...dependencies import get_current_user

router = APIRouter()


def check_project_access(project_id: int, user: UserModel, db: Session) -> ProjectModel:
    """Check if user has access to project"""
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check if user is project member
    is_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user.id
    ).first()
    
    if not is_member:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return project


def check_board_access(board_id: int, user: UserModel, db: Session) -> BoardModel:
    """Check if user has access to board"""
    board = db.query(BoardModel).filter(BoardModel.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    check_project_access(board.project_id, user, db)
    return board


@router.get("/project/{project_id}", response_model=List[Board])
def get_project_boards(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Get all boards for a project"""
    check_project_access(project_id, current_user, db)
    
    boards = db.query(BoardModel).filter(
        BoardModel.project_id == project_id
    ).order_by(BoardModel.created_at).all()
    
    return boards


@router.get("/{board_id}", response_model=BoardWithColumns)
def get_board(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Get board with columns"""
    board = check_board_access(board_id, current_user, db)
    
    # Get columns
    columns = db.query(ColumnModel).filter(
        ColumnModel.board_id == board_id
    ).order_by(ColumnModel.position).all()
    
    return BoardWithColumns(
        **board.__dict__,
        columns=columns
    )


@router.post("/", response_model=Board, status_code=status.HTTP_201_CREATED)
def create_board(
    board_data: BoardCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Create a new board"""
    check_project_access(board_data.project_id, current_user, db)
    
    # Create board
    db_board = BoardModel(
        name=board_data.name,
        description=board_data.description,
        project_id=board_data.project_id,
        is_default=board_data.is_default,
    )
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    
    # Create default columns
    default_columns = [
        {"name": "К выполнению", "position": 0},
        {"name": "В работе", "position": 1},
        {"name": "Готово", "position": 2},
    ]
    
    for col_data in default_columns:
        column = ColumnModel(
            board_id=db_board.id,
            name=col_data["name"],
            position=col_data["position"],
        )
        db.add(column)
    
    db.commit()
    db.refresh(db_board)
    
    return db_board


@router.patch("/{board_id}", response_model=Board)
def update_board(
    board_id: int,
    board_data: BoardUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Update board"""
    board = check_board_access(board_id, current_user, db)
    
    update_data = board_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(board, field, value)
    
    db.commit()
    db.refresh(board)
    
    return board


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Delete board"""
    board = check_board_access(board_id, current_user, db)
    
    db.delete(board)
    db.commit()
    
    return None


# Column endpoints
@router.post("/columns", response_model=Column, status_code=status.HTTP_201_CREATED)
def create_column(
    column_data: ColumnCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Create a new column"""
    check_board_access(column_data.board_id, current_user, db)
    
    db_column = ColumnModel(
        board_id=column_data.board_id,
        name=column_data.name,
        position=column_data.position,
        wip_limit=column_data.wip_limit,
    )
    db.add(db_column)
    db.commit()
    db.refresh(db_column)
    
    return db_column


@router.patch("/columns/{column_id}", response_model=Column)
def update_column(
    column_id: int,
    column_data: ColumnUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Update column"""
    column = db.query(ColumnModel).filter(ColumnModel.id == column_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    
    check_board_access(column.board_id, current_user, db)
    
    update_data = column_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(column, field, value)
    
    db.commit()
    db.refresh(column)
    
    return column


@router.delete("/columns/{column_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_column(
    column_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Delete column"""
    column = db.query(ColumnModel).filter(ColumnModel.id == column_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    
    check_board_access(column.board_id, current_user, db)
    
    db.delete(column)
    db.commit()
    
    return None
