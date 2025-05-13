from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.crud.crud_permission import (
    crud_create_permission,
    crud_add_permission,
    crud_get_all_permissions,
    crud_get_permission_by_id,
    crud_update_permission,
    crud_delete_permission,
    crud_remove_permission_from_role
)
from app.schemas.schema_permission import (
    PermissionCreate,
    PermissionRead,
    RoleRolePermissionRead,
    RoleRolePermissionCreate
)
from app.models.user import User
from app.core.security import require_any_permission


router = APIRouter()


@router.post("/add-permission", response_model=PermissionRead)
def api_create_permission(
    permission_data: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_permission("MANAGE_PERMISSIONS"))
):
    return crud_create_permission(permission_data, db)


@router.post("/assignment", response_model=RoleRolePermissionCreate)
def api_assignments(
    data: RoleRolePermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_permission("MANAGE_PERMISSIONS"))
):
    return crud_add_permission(data, db)


@router.get("/all", response_model=list[PermissionRead])
def api_get_all_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_permission("MANAGE_PERMISSIONS"))
):
    return crud_get_all_permissions(db)


@router.get("/{permission_id}", response_model=PermissionRead)
def api_get_permission_by_id(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_permission("MANAGE_PERMISSIONS"))
):
    return crud_get_permission_by_id(permission_id, db)


@router.put("/{permission_id}", response_model=PermissionRead)
def api_update_permission(
    permission_id: int,
    permission_data: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_permission("MANAGE_PERMISSIONS"))
):
    return crud_update_permission(permission_id, permission_data, db)


@router.delete("/{permission_id}")
def api_delete_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_permission("MANAGE_PERMISSIONS"))
):
    return crud_delete_permission(permission_id, db)


@router.delete("/{role_id}/remove/{permission_id}")
def api_remove_permission_from_role(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_permission("MANAGE_PERMISSIONS"))
):
    return crud_remove_permission_from_role(role_id, permission_id, db)
