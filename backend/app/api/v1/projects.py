from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from ...database import get_db
from ...models.user import User as UserModel
from ...models.organization import Organization as OrgModel, OrganizationMember
from ...models.project import Project as ProjectModel, ProjectMember
from ...schemas.project import Project, ProjectCreate, ProjectUpdate
from ...dependencies import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=List[Project])
def get_user_projects(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Get all projects where user is a member"""
    # Get project IDs where user is a member
    project_memberships = db.query(ProjectMember.project_id).filter(
        ProjectMember.user_id == current_user.id
    ).all()
    
    project_ids = [pm.project_id for pm in project_memberships]
    
    if not project_ids:
        return []
    
    projects = db.query(ProjectModel).filter(
        ProjectModel.id.in_(project_ids)
    ).order_by(ProjectModel.created_at.desc()).all()
    
    return projects


@router.get("/{project_id}", response_model=Project)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Get project by ID"""
    # Check if user is project member
    is_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()
    
    if not is_member:
        raise HTTPException(status_code=403, detail="Access denied")
    
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project


@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Create a new project"""
    # Check if user is organization member
    is_org_member = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == project_data.organization_id,
        OrganizationMember.user_id == current_user.id
    ).first()
    
    if not is_org_member:
        raise HTTPException(
            status_code=403,
            detail="You must be an organization member to create projects"
        )
    
    # Check if project key is unique within organization
    existing = db.query(ProjectModel).filter(
        ProjectModel.organization_id == project_data.organization_id,
        ProjectModel.key == project_data.key
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Project key already exists in this organization"
        )
    
    # Create project
    db_project = ProjectModel(
        name=project_data.name,
        key=project_data.key,
        description=project_data.description,
        organization_id=project_data.organization_id,
        owner_id=current_user.id,
        status="active",
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Add creator as project admin
    project_member = ProjectMember(
        project_id=db_project.id,
        user_id=current_user.id,
        role="admin"
    )
    db.add(project_member)
    db.commit()
    
    return db_project


@router.patch("/{project_id}", response_model=Project)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Update project"""
    # Check if user is project admin
    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()
    
    if not member or member.role not in ["admin", "owner"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Delete project"""
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Only project owner can delete
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only project owner can delete")
    
    db.delete(project)
    db.commit()
    
    return None
