from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.schema_user import UserSignin
from app.core.config import settings
from app.models.user_role import UserRole
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.permission import Permission


oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

def crud_signin(user_data: UserSignin, db: Session):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not verify_password(user_data.password, user.hashed_password):  # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    user_roles = db.query(UserRole).filter(UserRole.user_id == user.id).all()
    role_ids = [ur.role_id for ur in user_roles]
    roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
    role_names = [role.name for role in roles]

    role_permissions = db.query(RolePermission).filter(RolePermission.role_id.in_(role_ids)).all()
    permission_ids = [rp.permission_id for rp in role_permissions]
    permissions = db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
    permission_names = [p.name for p in permissions]

    token = create_access_token(data={
        "sub": str(user.id),
        "username": user.username,
        "roles": role_names,
        "permissions": permission_names
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "name": user.full_name,
        "roles": role_names,
        "permissions": permission_names
    }
