from fastapi import APIRouter
from app.routers import images

api = APIRouter()
api.include_router(images.router, prefix="/images", tags=["images"])