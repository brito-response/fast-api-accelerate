def test_auth_controller_template() -> str:
    return """
import pytest
from unittest.mock import AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.modules.auth.controllers.auth_controller import AuthController
from src.core.container_ioc import get_auth_service


@pytest.fixture
def mock_auth_service():
    return AsyncMock()


@pytest.fixture
def app(mock_auth_service):
    app = FastAPI()
    controller = AuthController()
    app.include_router(controller.router)
    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service

    return app


@pytest.fixture
def client(app):
    return TestClient(app)


class TestAuthControllerLogin:

    def test_login_success(self, client, mock_auth_service):
        mock_auth_service.login.return_value = {"access_token": "access123","refresh_token": "refresh123"}

        response = client.post("/auth/login",json={"email": "test@email.com","password": "123","client_type": "web"})

        assert response.status_code == 200
        assert response.json()["access_token"] == "access123"
        assert response.json()["refresh_token"] == "refresh123"

class TestAuthControllerRefresh:

    def test_refresh_success(self, client, mock_auth_service):
        mock_auth_service.refresh.return_value = {"access_token": "new_access"}

        response = client.post("/auth/refresh",json={"refresh_token": "valid_refresh","client_type": "web"})

        assert response.status_code == 200
        assert response.json()["access_token"] == "new_access"

class TestAuthControllerMe:

    def test_me_success(self, app):
        app.dependency_overrides.clear()

        async def fake_current_user():
            return {"id": "1", "username": "test"}

        from src.core.container_ioc import get_current_user
        app.dependency_overrides[get_current_user] = fake_current_user

        client = TestClient(app)

        response = client.get("/auth/me")

        assert response.status_code == 200
        assert response.json()["id"] == "1"

"""