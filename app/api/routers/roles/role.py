from fastapi import Depends , APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.schema_role import RoleCreate, RoleRead, RoleUserCreate, RoleUserRead
from app.crud.crud_roles import (
    crud_create_role,
    crud_add_roles,
    crud_get_all_roles,
    crud_get_role_by_id,
    crud_update_role,
    crud_delete_role,
    crud_remove_role_from_user,
    crud_get_all_roles_by_user
)
from app.core.database import get_db
from app.core.security import require_any_permission
from app.models.user import User
from uuid import UUID

router = APIRouter()

@router.post("/add-roles" ,response_model=RoleRead)
def api_create_role(role_data: RoleCreate, db: Session = Depends(get_db), current_user: User = Depends(require_any_permission("MANAGE_PERMISSIONS"))):
    return crud_create_role(role_data, db)


@router.post("/assignment" , response_model=RoleUserRead)
def api_assignment_role(data: RoleUserCreate, db: Session = Depends(get_db), current_user: User = Depends(require_any_permission("MANAGE_PERMISSIONS"))):
    return crud_add_roles(data, db)


@router.get("/all", response_model=list[RoleRead])
def api_get_all_roles(db: Session = Depends(get_db), current_user: User = Depends(require_any_permission("MANAGE_PERMISSIONS"))):
    return crud_get_all_roles(db)


@router.get("/{role_id}", response_model=RoleRead)
def api_get_role_by_id(role_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_any_permission("MANAGE_PERMISSIONS"))):
    return crud_get_role_by_id(role_id, db)


@router.put("/{role_id}", response_model=RoleRead)
def api_update_role(role_id: UUID, role_data: RoleCreate, db: Session = Depends(get_db), current_user: User = Depends(require_any_permission("MANAGE_PERMISSIONS"))):
    return crud_update_role(role_id, role_data, db)


@router.delete("/{role_id}")
def api_delete_role(role_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_any_permission("MANAGE_PERMISSIONS"))):
    return crud_delete_role(role_id, db)


@router.delete("/{user_id}/remove/{role_id}")
def api_remove_role_from_user(user_id: UUID, role_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_any_permission("MANAGE_PERMISSIONS"))):
    return crud_remove_role_from_user(user_id, role_id, db)

@router.get("/user/{user_id}", response_model=list[RoleRead])
def api_get_roles_by_user_id(user_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_any_permission("MANAGE_PERMISSIONS"))):
    return crud_get_all_roles_by_user(user_id, db)

