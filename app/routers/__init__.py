from fastapi import APIRouter
from .images import router as images_router


api = APIRouter()
api.include_router(images_router, prefix="/images", tags=["images"])