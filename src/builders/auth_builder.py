from pathlib import Path
from typing import Optional

from .base import BaseBuilder
from ..utils.file_system import FileSystem
from ..templates import user_model_template, user_schemas_template


class AuthBuilder(BaseBuilder):
    def __init__(self,base_path: Path,jwt: bool = True,refresh_token: bool = True,roles: bool = True,async_db: bool = True):
        self.base_path = base_path
        self.jwt = jwt
        self.refresh_token = refresh_token
        self.roles = roles
        self.async_db = async_db

        self.auth_path = self.base_path / "app" / "modules" / "auth"
        self.fs = FileSystem()

    def build(self):
        self._create_structure()
        self._create_user_model()
        self._create_schemas()
        self._create_security_files()
        self._create_repository()
        self._create_service()
        self._create_dependencies()
        self._create_controller()
        self._create_routes()
        self._register_router()
        self._install_dependencies()

    def _create_structure(self):
        folders = ["controllers","services","repositories","schemas","models","dependencies","security"]

        for folder in folders:
            self.fs.create_dir(self.auth_path / folder)


    def _create_user_model(self):
        self.fs.create_file(self.auth_path / "models" / "user_model.py", user_model_template)

    def _create_schemas(self):
        self.fs.create_file(self.auth_path / "schemas" / "auth_dto.py", user_schemas_template)

    def _create_security_files(self):
        jwt_handler = """from datetime import datetime, timedelta
        from jose import jwt
        from app.core.config import settings

        ALGORITHM = "HS256"


        def create_access_token(data: dict, expires_delta: int = 15):
            to_encode = data.copy()
            expire = datetime.utcnow() + timedelta(minutes=expires_delta)
            to_encode.update({"exp": expire})
            return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


        def decode_token(token: str):
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        """
        self.fs.create_file(self.auth_path / "security" / "jwt_handler.py", jwt_handler)

        password_hasher = """from passlib.context import CryptContext

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


        def hash_password(password: str):
            return pwd_context.hash(password)


        def verify_password(plain_password: str, hashed_password: str):
            return pwd_context.verify(plain_password, hashed_password)
        """
        self.fs.create_file(self.auth_path / "security" / "password_hasher.py",password_hasher)


    def _create_repository(self):
        content = """from sqlalchemy.ext.asyncio import AsyncSession
        from sqlalchemy import select
        from app.modules.auth.models.user_model import User


        class UserRepository:

            def __init__(self, db: AsyncSession):
                self.db = db

            async def get_by_email(self, email: str):
                result = await self.db.execute(select(User).where(User.email == email))
                return result.scalar_one_or_none()

            async def create(self, user: User):
                self.db.add(user)
                await self.db.commit()
                await self.db.refresh(user)
                return user
        """
        self.fs.create_file(self.auth_path / "repositories" / "user_repository.py",content)

    def _create_service(self):
        content = """from sqlalchemy.ext.asyncio import AsyncSession
        from app.modules.auth.repositories.user_repository import UserRepository
        from app.modules.auth.security.password_hasher import hash_password, verify_password
        from app.modules.auth.security.jwt_handler import create_access_token
        from app.modules.auth.models.user_model import User

        class AuthService:

            def __init__(self, db: AsyncSession):
                self.repo = UserRepository(db)

            async def register_user(self, email: str, password: str):
                hashed = hash_password(password)
                user = User(email=email, password_hash=hashed)
                return await self.repo.create(user)

            async def authenticate_user(self, email: str, password: str):
                user = await self.repo.get_by_email(email)
                if not user:
                    return None

                if not verify_password(password, user.password_hash):
                    return None

                return user

            async def generate_token(self, user: User):
                return create_access_token({"sub": str(user.id)})
        """
        self.fs.create_file(self.auth_path / "services" / "auth_service.py",content)


    def _create_dependencies(self):
        content = """from fastapi import Depends, HTTPException, status
        from jose import JWTError
        from sqlalchemy.ext.asyncio import AsyncSession
        from app.core.database import get_db
        from app.modules.auth.security.jwt_handler import decode_token
        from app.modules.auth.repositories.user_repository import UserRepository


        async def get_current_user(token: str, db: AsyncSession = Depends(get_db)):
            try:
                payload = decode_token(token)
                user_id = payload.get("sub")
            except JWTError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            repo = UserRepository(db)
            user = await repo.get_by_email(user_id)

            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            return user
        """
        self.fs.create_file(self.auth_path / "dependencies" / "get_current_user.py",content)

    def _create_controller(self):
        content = """from fastapi import APIRouter, Depends
        from sqlalchemy.ext.asyncio import AsyncSession
        from app.core.database import get_db
        from app.modules.auth.schemas.auth_dto import RegisterDTO, LoginDTO
        from app.modules.auth.services.auth_service import AuthService

        router = APIRouter(prefix="/auth", tags=["Auth"])


        @router.post("/register")
        async def register(data: RegisterDTO, db: AsyncSession = Depends(get_db)):
            service = AuthService(db)
            return await service.register_user(data.email, data.password)


        @router.post("/login")
        async def login(data: LoginDTO, db: AsyncSession = Depends(get_db)):
            service = AuthService(db)
            user = await service.authenticate_user(data.email, data.password)
            if not user:
                return {"error": "Invalid credentials"}

            token = await service.generate_token(user)
            return {"access_token": token}
        """
        self.fs.create_file(self.auth_path / "controllers" / "auth_controller.py",content)

    def _create_routes(self):
        content = """from app.modules.auth.controllers.auth_controller import router"""
        self.fs.create_file(self.auth_path / "routes.py", content)


    def _register_router(self):
        main_path = self.base_path / "app" / "main.py"

        if not main_path.exists():
            return

        self.fs.append_to_file(main_path,"\nfrom app.modules.auth.routes import router as auth_router\napp.include_router(auth_router)\n")


    def _install_dependencies(self):
        deps = ["python-jose[cryptography]","passlib[bcrypt]","python-multipart"]
        self.fs.install_dependencies(deps)