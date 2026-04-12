from fastapi import APIRouter, Depends, Query

from app.services.video_service import VideoService


video_router = APIRouter(prefix="/videos", tags=["videos"])


def get_video_service():
    return VideoService()


@video_router.get("/info")
async def get_info(
    url: str = Query(..., description="Video URL"),
    service: VideoService = Depends(get_video_service),
):
    return await service.get_info(url)


@video_router.get("/stream")
async def stream_video(
    url: str = Query(..., description="Link to original video to be streamed"),
    service: VideoService = Depends(get_video_service),
):
    return await service.stream_video(url)
