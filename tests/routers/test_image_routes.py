from fastapi import Response
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


def test_proxy_route_missing_params():
    # Test to see if a 422 error is reported if the 'url' parameter is missing.
    response = client.get("/api/v1/images/proxy")
    assert response.status_code == 422


@patch("app.services.image_service.ImageService.proxy_image")
def test_proxy_route_call_service(mock_proxy):
    # Simulate the return results from the service.
    mock_proxy.return_value = Response(content=b"data", media_type="image/jpeg")

    test_url = "https://test.com/img.jpg"
    response = client.get(f"/api/v1/images/proxy?url={test_url}")

    assert response.status_code == 200
    assert response.content == b"data"
    # Check if the router is actually calling the service with the correct URL.
    mock_proxy.assert_called_once_with(test_url)
