def auth_service_template()->str:
    return """from datetime import datetime, timedelta, UTC
from typing import Dict, Any
from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from src.modules.users.repositories import UserRepository
from  src.modules.auth.utils.client_type import ClientType

class AuthService:

    SECRET_KEY = "test-secret-key"
    ALGORITHM = "HS256"
    TOKEN_EXPIRATION_POLICY = {
        ClientType.WEB: {"access": timedelta(minutes=30),"refresh": timedelta(days=7)},
        ClientType.MOBILE: {"access": timedelta(minutes=60),"refresh": timedelta(days=15)},
    }
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        if not plain_password or not hashed_password:
            return False
        try:
            return self.pwd_context.verify(plain_password, hashed_password)
        except ValueError:
            return False

    def _create_token(self,data: Dict[str, Any],token_type: str,client_type: ClientType) -> str:

        if not data or "id" not in data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid payload")

        if client_type not in self.TOKEN_EXPIRATION_POLICY:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid client type")

        expire_delta = self.TOKEN_EXPIRATION_POLICY[client_type][token_type]
        expire = datetime.now(UTC) + expire_delta
        to_encode = data.copy()
        to_encode.update({"exp": expire,"type": token_type,"client": client_type.value})

        return jwt.encode(to_encode,self.SECRET_KEY,algorithm=self.ALGORITHM )

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token,self.SECRET_KEY,algorithms=[self.ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token")

    async def login(self,email: str,password: str,client_type: ClientType) -> Dict[str, str]:

        user = await self.repository.get_by_email(email)
        if not user or not self.verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Credenciais inválidas")

        access_claims = {"id": str(user.id),"username": user.username,"email": user.email,"image": user.image,"roles": user.roles if isinstance(user.roles, list) else [user.roles],"userStatus": user.status}

        refresh_claims = {"id": str(user.id)}
        access_token = self._create_token(access_claims,token_type="access",client_type=client_type)
        refresh_token = self._create_token(refresh_claims,token_type="refresh",client_type=client_type)

        return {"access_token": access_token,"refresh_token": refresh_token}

    async def refresh(self,refresh_token: str,client_type: ClientType) -> Dict[str, str]:
        payload = self.decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token type")

        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token payload")

        user = await self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")

        access_claims = {"id": str(user.id),"username": user.username,"email": user.email,"image": user.image,"roles": user.roles if isinstance(user.roles, list) else [user.roles],"userStatus": user.status}
        new_access_token = self._create_token(access_claims,token_type="access",client_type=client_type)

        return {"access_token": new_access_token}
"""