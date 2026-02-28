def config_container_ioc_template(name_resource:str="") -> str:
    return """from typing import AsyncGenerator
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.configs import settings
from src.modules.users.repositories import UserRepository
from src.modules.users.services import UserService
from src.modules.auth.services import AuthService


bearer_scheme = HTTPBearer()

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with settings.async_session_factory() as session:
        yield session

#TODO: --------> todo recurso vai exigir repository e serviço

def get_user_repository(db: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db)

def get_users_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository)

#TODO: --------> até isso aqui ref ->  get_auth_service

def get_auth_service(repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(repository)

def get_token_from_header(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    return credentials.credentials

async def get_current_user(token: str = Depends(get_token_from_header),auth_service: AuthService = Depends(get_auth_service)):
    payload = await auth_service.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="invalid token")
    return payload


def role_required(allowed_roles: list[str]):
    def dependency(current_user: dict = Depends(get_current_user)):
        user_roles = current_user.get("roles", [])
        if not any(role in user_roles for role in allowed_roles):
            raise HTTPException(status_code=403, detail="Not authorization")
        return current_user
    return dependency

"""