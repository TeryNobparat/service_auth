from datetime import datetime, timedelta
from jose import JWTError,jwt
from passlib.context import CryptContext
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.user_role import UserRole
from app.models.role_permission import RolePermission
from app.models.permission import Permission
from app.models.role import Role
from app.core.database import get_db
from app.core.config import settings
from typing import Optional,List,Dict,Any


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password : str) -> bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = dict(data)
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # type: ignore
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication expired credentials")

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    user_id = decode_access_token(token).get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id).all()

    role_ids = [ur.role_id for ur in user_roles]  # 🟢 เปลี่ยนจาก ur.role.id เป็น ur.role_id
    roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
    role_names = [role.name for role in roles]

    role_permissions = db.query(RolePermission).filter(RolePermission.role_id.in_(role_ids)).all()

    permissions_ids = [rp.permission_id for rp in role_permissions]
    permissions = db.query(Permission).filter(Permission.id.in_(permissions_ids)).all()
    permission_names = [permission.name for permission in permissions]

    return {
        "user_id": str(user.id),
        "username": user.username,
        "roles": role_names,
        "role_ids": role_ids, 
        "permissions": permission_names
    }

def require_any_permission(*perms):
    def cheker(user: User = Depends(get_current_user)):
        if not any(p in user["permissions"] for p in perms):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied !!"
            )
        return user
    return cheker


