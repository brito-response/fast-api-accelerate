def test_auth_service_template() -> str:
    return """
import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from modules.auth.services.auth_service import AuthService, ClientType

@pytest.fixture
def mock_repository():
    return AsyncMock()

@pytest.fixture
def auth_service(mock_repository):
    return AuthService(repository=mock_repository)

class TestAuthServiceLogin:

    @pytest.mark.asyncio
    async def test_login_success(self, auth_service, mock_repository, mocker):
        # given
        user = MagicMock()
        user.id = 1
        user.password = "hashed_password"
        user.username = "test"
        user.email = "test@email.com"
        user.image = "img.png"
        user.roles = ["admin"]
        user.status = "ACTIVE"
        mock_repository.get_by_email.return_value = user
        mocker.patch.object(auth_service, "verify_password", return_value=True)
        mocker.patch.object(auth_service, "_create_token", side_effect=["access123", "refresh123"])

        result = await auth_service.login("test@email.com","123",ClientType.WEB) # when

        # then
        assert result["access_token"] == "access123"
        assert result["refresh_token"] == "refresh123"

    @pytest.mark.asyncio
    async def test_login_user_not_found(self, auth_service, mock_repository):
        mock_repository.get_by_email.return_value = None

        with pytest.raises(HTTPException) as exc:
            await auth_service.login("no@user.com","123",ClientType.WEB)

        assert exc.value.status_code == 401

    @pytest.mark.asyncio
    async def test_login_invalid_password(self, auth_service, mock_repository, mocker):
        # given
        user = MagicMock()
        user.id = 1
        user.password = "hashed"
        user.username = "test"
        user.email = "test@email.com"
        user.image = "img.png"
        user.roles = []
        user.status = "ACTIVE"

        mock_repository.get_by_email.return_value = user
        mocker.patch.object(auth_service, "verify_password", return_value=False)

        # when
        with pytest.raises(HTTPException) as exc: 
            await auth_service.login("test@email.com","wrong",ClientType.WEB)

        assert exc.value.status_code == 401 # then

class TestAuthServicePassword:

    def test_verify_password_correct(self, auth_service, mocker):
        mocker.patch.object(auth_service.pwd_context,"verify",return_value=True) # when
        assert auth_service.verify_password("123", "hashed") is True # then

    def test_verify_password_incorrect(self, auth_service, mocker):
        mocker.patch.object(auth_service.pwd_context,"verify",return_value=False) # when
        assert auth_service.verify_password("123", "hashed") is False # then

    def test_verify_password_exception(self, auth_service, mocker):
        mocker.patch.object(auth_service.pwd_context,"verify",side_effect=ValueError("Invalid hash"))  # when
        assert auth_service.verify_password("123", "invalid_hash") is False # then

class TestAuthServiceTokens:

    def test_create_token_success(self, auth_service, mocker):
        mocker.patch("modules.auth.services.auth_service.jwt.encode",return_value="token123")

        token = auth_service._create_token({"id": "1"},token_type="access",client_type=ClientType.WEB)

        assert token == "token123"

    def test_create_token_invalid_payload(self, auth_service):
        with pytest.raises(HTTPException):
            auth_service._create_token({},token_type="access",client_type=ClientType.WEB)

class TestAuthServiceRefresh:

    @pytest.mark.asyncio
    async def test_refresh_success(self, auth_service, mock_repository, mocker):
        mocker.patch.object(auth_service,"decode_token",return_value={"id": "1", "type": "refresh"})

        user = MagicMock()
        user.id = 1
        user.username = "updated"
        user.email = "updated@email.com"
        user.image = "new.png"
        user.roles = ["admin"]
        user.status = "ACTIVE"

        mock_repository.get_by_id.return_value = user

        mocker.patch.object(auth_service, "_create_token", return_value="new_access")

        result = await auth_service.refresh("valid_refresh_token",ClientType.WEB)

        assert result["access_token"] == "new_access"

    @pytest.mark.asyncio
    async def test_refresh_invalid_type(self, auth_service, mocker):
        mocker.patch.object(auth_service,"decode_token",return_value={"id": "1", "type": "access"})

        with pytest.raises(HTTPException) as exc:
            await auth_service.refresh("invalid_token",ClientType.WEB)

        assert exc.value.status_code == 401

    @pytest.mark.asyncio
    async def test_refresh_user_not_found(self, auth_service, mock_repository, mocker):
        # given
        mocker.patch.object(auth_service,"decode_token",return_value={"id": "1", "type": "refresh"})
        mock_repository.get_by_id.return_value = None

        with pytest.raises(HTTPException) as exc: # when
            await auth_service.refresh("valid_refresh",ClientType.WEB)

        assert exc.value.status_code == 401 # then
"""