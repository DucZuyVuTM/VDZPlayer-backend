from fastapi import APIRouter, Depends, Query

from app.services.image_service import ImageService


image_router = APIRouter(prefix="/images", tags=["images"])


def get_image_service():
    return ImageService()


@image_router.get("/proxy")
async def proxy_image(
    url: str = Query(..., description="Link to original image to be proxied"),
    service: ImageService = Depends(get_image_service),
):
    return await service.proxy_image(url)
