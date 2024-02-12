from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from src.main import app

def test_get_user_info():
    with TestClient(app) as client:
        mock_response_data = {"user": "John Doe"}
        mock_find_bitpapa_token = AsyncMock(return_value="mocked_token")

        with patch("src.repo.service.find_bitpapa_token", mock_find_bitpapa_token), \
                patch("httpx.AsyncClient") as mock_async_client:
            mock_async_client.return_value.get.return_value = AsyncMock(
                status_code=200,
                json=AsyncMock(return_value=mock_response_data)
            )

            response = client.get("/bitpapa/get-user-info")

            assert response.status_code == 200

            mock_find_bitpapa_token.assert_called_once()

            assert response.json() == mock_response_data

