import pytest
from fastapi import HTTPException
from unittest.mock import AsyncMock, patch

from app.services.image_service import ImageService


@pytest.mark.asyncio
async def test_proxy_image_success():
    service = ImageService()
    url = "https://example.com/photo.jpg"

    # Simulated successful response from httpx.
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.content = b"fake_image_binary"
    mock_response.headers = {"Content-Type": "image/png"}

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        response = await service.proxy_image(url)
        assert response.status_code == 200
        assert response.body == b"fake_image_binary"
        assert response.media_type == "image/png"


@pytest.mark.asyncio
async def test_proxy_image_fetch_error():
    service = ImageService()
    url = "https://example.com/notfound.jpg"

    # Simulate a 404 error response.
    mock_response = AsyncMock()
    mock_response.status_code = 404

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        with pytest.raises(HTTPException) as exc:
            await service.proxy_image(url)
        assert exc.value.status_code == 404
        assert exc.value.detail == "Could not fetch image"
