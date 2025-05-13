from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schema_role import RoleCreate, RoleRead,RoleUserCreate,RoleUserRead
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole
from uuid import UUID


def crud_create_role(role_data: RoleCreate, db: Session) -> RoleRead:
    role = db.query(Role).filter(Role.name == role_data.name).first()
    if role:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Roles already exists")

    new_role = Role(**role_data.dict())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return RoleRead.from_orm(new_role)



def crud_add_roles(data: RoleUserCreate, db: Session):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID does not exist in server!!"
        )

    role = db.query(Role).filter(Role.id == data.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role does not exist!!"
        )

    user_role = db.query(UserRole).filter(
        UserRole.user_id == data.user_id,
        UserRole.role_id == data.role_id
    ).first()
    if user_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request is duplicate!!"
        )

    new_assignment = UserRole(**data.dict())
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return RoleUserRead.from_orm(new_assignment)



def crud_get_all_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return [RoleRead.from_orm(r) for r in roles]

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
    db.delete(role)
    db.commit()
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
