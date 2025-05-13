from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission

from app.schemas.schema_permission import PermissionCreate, PermissionRead, RoleRolePermissionCreate, RoleRolePermissionRead


def crud_create_permission(permission_data: PermissionCreate, db: Session = Depends(get_db)):
    permis = db.query(Permission).filter(Permission.name == permission_data.name).first()

    if permis:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="permission already !!")

    new_permission = Permission(**permission_data.dict())
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return PermissionRead.from_orm(new_permission)


def crud_add_permission(data: RoleRolePermissionCreate, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == data.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not have Role !!"
        )

    perm = db.query(Permission).filter(Permission.id == data.permission_id).first()

    if not perm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not have Permission !!"
        )

    new_assignment = RolePermission(**data.dict())
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return RoleRolePermissionRead.from_orm(new_assignment)


def crud_get_all_permissions(db: Session = Depends(get_db)):
    permissions = db.query(Permission).all()
    return [PermissionRead.from_orm(p) for p in permissions]


def crud_get_permission_by_id(permission_id: int, db: Session = Depends(get_db)):
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return PermissionRead.from_orm(permission)


def crud_update_permission(permission_id: int, permission_data: PermissionCreate, db: Session = Depends(get_db)):
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    for key, value in permission_data.dict().items():
        setattr(permission, key, value)

    db.commit()
    db.refresh(permission)
    return PermissionRead.from_orm(permission)


def crud_delete_permission(permission_id: int, db: Session = Depends(get_db)):
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    db.delete(permission)
    db.commit()
    return {"detail": "Permission deleted"}


def crud_remove_permission_from_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    assignment = db.query(RolePermission).filter(
        RolePermission.role_id == role_id,
        RolePermission.permission_id == permission_id
    ).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Permission assignment not found")

    db.delete(assignment)
    db.commit()
    return {"detail": "Permission removed from role"}
