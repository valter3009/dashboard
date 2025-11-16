"""Organization API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.organization import (
    Organization,
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationWithMembers,
    OrganizationMember,
    OrganizationMemberCreate,
)
from app.models.organization import Organization as OrgModel, OrganizationMember as OrgMemberModel
from app.models.user import User as UserModel
from app.dependencies import get_current_active_user
from app.utils.constants import UserRole

router = APIRouter()


@router.post("/", response_model=Organization, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org_data: OrganizationCreate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new organization."""
    # Create organization
    org = OrgModel(
        **org_data.model_dump(),
        owner_id=current_user.id
    )
    db.add(org)
    db.flush()

    # Add creator as owner
    member = OrgMemberModel(
        organization_id=org.id,
        user_id=current_user.id,
        role=UserRole.OWNER
    )
    db.add(member)
    db.commit()
    db.refresh(org)

    return org


@router.get("/", response_model=List[Organization])
async def list_organizations(
    skip: int = 0,
    limit: int = 50,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List organizations where user is a member."""
    # Get user's organization memberships
    memberships = db.query(OrgMemberModel).filter(
        OrgMemberModel.user_id == current_user.id
    ).all()

    org_ids = [m.organization_id for m in memberships]
    orgs = db.query(OrgModel).filter(OrgModel.id.in_(org_ids)).offset(skip).limit(limit).all()

    return orgs


@router.get("/{org_id}", response_model=OrganizationWithMembers)
async def get_organization(
    org_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get organization by ID."""
    org = db.query(OrgModel).filter(OrgModel.id == org_id).first()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    # Check if user is a member
    is_member = db.query(OrgMemberModel).filter(
        OrgMemberModel.organization_id == org_id,
        OrgMemberModel.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this organization"
        )

    return org


@router.put("/{org_id}", response_model=Organization)
async def update_organization(
    org_id: int,
    org_update: OrganizationUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update organization."""
    # TODO: Check if user has permission to update (owner or admin)
    org = db.query(OrgModel).filter(OrgModel.id == org_id).first()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    update_data = org_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(org, field, value)

    db.commit()
    db.refresh(org)

    return org


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    org_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete organization."""
    # TODO: Check if user is owner
    org = db.query(OrgModel).filter(OrgModel.id == org_id).first()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    db.delete(org)
    db.commit()


@router.post("/{org_id}/members", response_model=OrganizationMember, status_code=status.HTTP_201_CREATED)
async def add_organization_member(
    org_id: int,
    member_data: OrganizationMemberCreate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add member to organization."""
    # TODO: Check if current user has permission to add members
    # Create member
    member = OrgMemberModel(
        organization_id=org_id,
        **member_data.model_dump()
    )
    db.add(member)
    db.commit()
    db.refresh(member)

    return member


@router.get("/{org_id}/members", response_model=List[OrganizationMember])
async def list_organization_members(
    org_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List organization members."""
    members = db.query(OrgMemberModel).filter(
        OrgMemberModel.organization_id == org_id
    ).all()

    return members
