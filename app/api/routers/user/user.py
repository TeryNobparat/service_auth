from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.crud.crud_user import (
    crud_user_registor,
    crud_change_password,
    crud_edit_user,
    crud_get_user_by_id,
    crud_delete_user,
    crud_user_get_all,
    crud_user_remove_role,
    crud_assignment_role
)
from app.schemas.schema_user import UserCreate, UserRead, UserChangePassword, UserUpdate

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=201)
def api_register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    return crud_user_registor(user_create, db)


@router.post("/{user_id}/change-password", response_model=UserRead, status_code=200)
def api_change_password(user_id: UUID, password_data: UserChangePassword, db: Session = Depends(get_db)):
    return crud_change_password(user_id, password_data, db)


@router.post("/{user_id}/edit-detail", response_model=UserRead, status_code=200)
def api_edit_user(user_id: UUID, userupdate: UserUpdate, db: Session = Depends(get_db)):
    return crud_edit_user(user_id, userupdate, db)


@router.get("/all", response_model=list[UserRead])
def api_get_all_users(db: Session = Depends(get_db)):
    return crud_user_get_all(db)


@router.get("/{user_id}", response_model=UserRead)
def api_get_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    return crud_get_user_by_id(user_id, db)


@router.delete("/{user_id}")
def api_delete_user(user_id: UUID, db: Session = Depends(get_db)):
    return crud_delete_user(user_id, db)


@router.delete("/{user_id}/remove-role/{role_id}")
def api_user_remove_role(user_id: UUID, role_id: UUID, db: Session = Depends(get_db)):
    return crud_user_remove_role(user_id, role_id, db)

@router.post("/{user_id}/roles")
def api_assign_roles(user_id:UUID, data: List[UUID], db: Session = Depends(get_db)):
    return crud_assignment_role(user_id,data,db)