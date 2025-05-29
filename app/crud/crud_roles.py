from unittest import result
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session,joinedload
from app.core.database import get_db
from app.models.pagerole import PageRole
from app.schemas.schema_permission import RolePermission
from app.schemas.schema_role import RoleCreate, RoleRead,RoleUserCreate,RoleUserRead
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole
from app.models.role_permission import RolePermission
from uuid import UUID
from typing import List


def crud_create_role(role_data: RoleCreate, db: Session) -> RoleRead:
    role = db.query(Role).filter(Role.name == role_data.name).first()
    if role:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Roles already exists")

    new_role = Role(**role_data.dict())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return RoleRead.from_orm(new_role)
    
def crud_assign_permission(roleId: UUID, permissionList: List[UUID], db: Session):
    db.query(RolePermission).filter(RolePermission.role_id == roleId).delete()
    db.commit()

    for permission_id in permissionList:
        new_role_permission = RolePermission(role_id=roleId, permission_id=permission_id) 
        db.add(new_role_permission)

    db.commit() 
    return {"detail": "Permission reassigned successfully"}

def crud_assign_pages(roleId: UUID, pagesList: List[UUID], db: Session):
    db.query(PageRole).filter(PageRole.role_id == roleId).delete()
    db.commit()

    for page_id in pagesList:
        new_role_pages = PageRole(role_id=roleId, page_id=page_id) 
        db.add(new_role_pages)

    db.commit() 
    return {"detail": "Permission reassigned successfully"}


def crud_get_all_roles(db: Session) -> list[dict]:
    roles = db.query(Role).options(
        joinedload(Role.permissions),
        joinedload(Role.pages)
        ).all() 
    result = []
    for role in roles:
        result.append({
            "id": role.id,
            "name": role.name,
            "permissions": [permission.id for permission in role.permissions], 
            "pages": [page.id for page in role.pages] 
        })
    return result

def crud_get_all_roles_by_user(user_id: UUID, db: Session = Depends(get_db)):
    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id).all()
    if not user_roles:
        raise HTTPException(status_code=404, detail="No roles found for the user")

    roles = [db.query(Role).filter(Role.id == user_role.role_id).first() for user_role in user_roles]
    return [RoleRead.from_orm(role) for role in roles if role]


def crud_get_role_by_id(role_id: UUID, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return RoleRead.from_orm(role)


def crud_update_role(role_id: UUID, role_data: RoleCreate, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    for key, value in role_data.dict().items():
        setattr(role, key, value)

    db.commit()
    db.refresh(role)
    return RoleRead.from_orm(role)



def crud_delete_role(role_id: UUID, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    try:
        db.query(RolePermission).filter(RolePermission.role_id == role.id).delete(synchronize_session=False)
        db.delete(role)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting role") from e

    return {"detail": "Role deleted"}



def crud_remove_role_from_user(user_id: UUID, role_id: UUID, db: Session = Depends(get_db)):
    assignment = db.query(UserRole).filter(
        UserRole.user_id == user_id,
        UserRole.role_id == role_id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="User-Role assignment not found")

    db.delete(assignment)
    db.commit()
    return {"detail": "Role removed from user"}
