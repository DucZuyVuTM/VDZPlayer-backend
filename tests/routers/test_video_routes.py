from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app

client = TestClient(app)

def test_video_info_route_missing_params():
    response = client.get("/api/v1/videos/info")
    assert response.status_code == 422

def test_proxy_route_missing_params():
    response = client.get("/api/v1/videos/stream")
    assert response.status_code == 422

def test_get_video_info_route():
    test_url = "https://facebook.com/watch?v=123"
    fake_data = {"id": "123", "title": "Cool Video"}
    
    with patch("app.services.video_service.VideoService.get_info", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = fake_data
        response = client.get(f"/api/v1/videos/info?url={test_url}")
        
        assert response.status_code == 200
        assert response.json() == fake_data
        mock_get.assert_called_once_with(test_url)

def test_stream_video_route():
    test_url = "https://example.com/file.mp4"
    
    with patch("app.services.video_service.VideoService.stream_video", new_callable=AsyncMock) as mock_stream:
        from fastapi.responses import StreamingResponse
        async def fake_gen(): yield b"data"
        mock_stream.return_value = StreamingResponse(fake_gen(), media_type="video/mp4")
        
        response = client.get(f"/api/v1/videos/stream?url={test_url}")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "video/mp4"
