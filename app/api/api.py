from fastapi import APIRouter
from api.endpoints import user


api_router = APIRouter()
api_router.include_router(user.router, prefix="/api/user", tags=["user"])
api_router.include_router(user.router, prefix="/api/ticket", tags=["ticket"])
api_router.include_router(user.router, prefix="/api/venue", tags=["venue"])
api_router.include_router(user.router, prefix="/api/contactperson", tags=["contactperson"])
