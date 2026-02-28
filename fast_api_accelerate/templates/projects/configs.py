def config_conection_template() -> str:
    return """from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from functools import lru_cache


class Settings(BaseSettings):
    # Credenciais do banco de dados (deve existir no .env)
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # Nova base declarativa do SQLAlchemy 2.0
    class BaseDB(DeclarativeBase):
        pass

    # Configuração do Pydantic v2
    model_config = SettingsConfigDict(case_sensitive=True,env_file=".env",extra="ignore")

    # URL de conexão do PostgreSQL usando asyncpg
    @property
    def DB_URL(self) -> str:
        return (f"postgresql+asyncpg://{self.DB_USER}:"f"{self.DB_PASSWORD}@{self.DB_HOST}:"f"{self.DB_PORT}/{self.DB_NAME}")

    # Engine singleton (criado apenas uma vez)
    @property
    @lru_cache
    def engine(self):
        return create_async_engine(self.DB_URL, echo=True)

    # Fábrica de sessões assíncronas singleton
    @property
    @lru_cache
    def async_session_factory(self):
        return sessionmaker(bind=self.engine,class_=AsyncSession,expire_on_commit=False)


# Singleton das configurações
@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
"""