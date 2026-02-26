def auth_controller_template() -> str:
    return """
from fastapi import APIRouter, Depends
from src.modules.auth.services import AuthService
from ..dtos import LoginRequest, RefreshRequest, TokenResponse,RefreshTokenResponse
from src.core.container_ioc import get_auth_service, get_current_user


class AuthController:

    def __init__(self):
        self.router = APIRouter(prefix="/auth",tags=["Auth"])
        self._register_routes()

    def _register_routes(self):

        @self.router.post("/login", response_model=TokenResponse)
        async def login(credentials: LoginRequest,service: AuthService = Depends(get_auth_service)):
            return await service.login(credentials.email,credentials.password,credentials.client_type)

        @self.router.post("/refresh", response_model=RefreshTokenResponse)
        async def refresh(request: RefreshRequest,service: AuthService = Depends(get_auth_service)):
            return await service.refresh(request.refresh_token,request.client_type)

        @self.router.get("/me")
        async def me(current_user=Depends(get_current_user)):
            return current_user

        @self.router.post("/logout")
        async def logout(current_user=Depends(get_current_user)):
            return {"detail": "Logout realizado com sucesso"}

"""