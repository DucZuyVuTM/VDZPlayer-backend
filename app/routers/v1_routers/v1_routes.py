from fastapi import APIRouter

from .image_routers.image_routes import image_router
from .video_routers.video_routes import video_router


v1_router = APIRouter(prefix="/v1")

v1_router.include_router(video_router)
v1_router.include_router(image_router)
