from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.user_role import UserRole
from app.models.role import Role
from app.schemas.schema_user import UserCreate, UserChangePassword, UserUpdate
from app.core.security import hash_password, verify_password
from app.models.user import User


def crud_user_registor(user_create: UserCreate, db: Session) -> User:
    existing_user = db.query(User).filter(User.username == user_create.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered !!")

    hashed_password = hash_password(user_create.password)

    new_user = User(
        username=user_create.username,
        full_name=user_create.full_name,
        table_tel=user_create.table_tel,
        fast_tel=user_create.fast_tel,
        email=user_create.email,
        hashed_password=hashed_password,
        is_active=user_create.is_active,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def crud_user_get_all(db: Session) -> list[User]:
    return db.query(User).all()


def crud_change_password(user_id: UUID, pwd_data: UserChangePassword, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not verify_password(pwd_data.old_password, user.hashed_password): # type: ignore
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")

    user.hashed_password = hash_password(pwd_data.new_password) # type: ignore

    db.commit()
    db.refresh(user)
    return user


def crud_edit_user(user_id: UUID, user_update: UserUpdate, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user

def crud_get_roles(user_id : UUID, db:Session):
    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id).all()
    role_ids = [ur.role.id for ur in user_roles]
    roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
    role_names = [role.name for role in roles]

    return {"role:": role_names} 


def crud_get_user_by_id(user_id: UUID, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def crud_delete_user(user_id: UUID, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}


def crud_user_remove_role(user_id: UUID, role_id: UUID, db: Session):
    assignment = db.query(UserRole).filter(
        UserRole.user_id == user_id,
        UserRole.role_id == role_id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Role assignment not found for user")

    db.delete(assignment)
    db.commit()
    return {"detail": "Role removed from user"}



