import pytest
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from unittest.mock import patch
from app.services.video_service import VideoService


@pytest.mark.asyncio
async def test_get_info_success():
    service = VideoService()
    url = "https://facebook.com/video123"
    fake_info = {"title": "Test Video", "thumbnail": "image.jpg"}

    with patch("app.services.video_service.get_video_info", return_value=fake_info):
        result = await service.get_info(url)
        assert result == fake_info


@pytest.mark.asyncio
async def test_get_info_invalid_url():
    service = VideoService()
    with patch("app.services.video_service.get_video_info", return_value=None):
        with pytest.raises(HTTPException) as exc:
            await service.get_info("invalid_url")
        assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_stream_video_invalid_url():
    service = VideoService()
    # Test with invalid URLs based on the code's logic.
    with pytest.raises(HTTPException) as exc:
        await service.stream_video("not_a_url")
    assert exc.value.status_code == 400
    assert exc.value.detail == "URL is invalid"
@pytest.mark.asyncio
async def test_stream_video_returns_streaming_response():
    service = VideoService()
    url = "https://example.com/video.mp4"

    response = await service.stream_video(url)
    assert isinstance(response, StreamingResponse)
    assert response.media_type == "video/mp4"
