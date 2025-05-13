from fastapi import APIRouter
from app.api.routers.user.user import router as user_router
from app.api.routers.user.auth import router as auth_router
from app.api.routers.roles.role import router as role_router
from app.api.routers.permission.permission import router as permission_router
from app.api.routers.page import router as page_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/user", tags=["Users"])
api_router.include_router(auth_router, prefix="/authentication", tags=["Authentication"])
api_router.include_router(role_router, prefix="/roles", tags=["Roles"])
api_router.include_router(permission_router, prefix="/permissions", tags=["Permissions"])
api_router.include_router(page_router, prefix="/pages", tags=["Pages"])

