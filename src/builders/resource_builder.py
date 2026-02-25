from pathlib import Path
from typing import List

from .base import BaseBuilder


class ResourceBuilder(BaseBuilder):
    """ Builder responsável por criar um CRUD completo async para um recurso. """

    def __init__(self,base_path: Path,resource_name: str,fields: List[str] | None = None,with_crud: bool = True):
        super().__init__(base_path)

        self.resource_name = resource_name.lower()
        self.class_name = resource_name.capitalize()
        self.fields = fields or []
        self.with_crud = with_crud

        self.module_path = (self.base_path / "app" / "modules" / self.resource_name)


    def build(self):
        self._create_structure()
        self._create_model()
        self._create_schemas()
        self._create_repository()
        self._create_service()

        if self.with_crud:
            self._create_controller()
            self._create_routes()
            self._register_router()

    def _create_structure(self):
        folders = [
            self.module_path,
            self.module_path / "models",
            self.module_path / "schemas",
            self.module_path / "repositories",
            self.module_path / "services",
            self.module_path / "controllers",
        ]

        self.ensure_structure(folders)

        for folder in folders:
            self.create_file(folder / "__init__.py", "")

    def _create_model(self):
        dynamic_fields = "\n".join(
            [
                f'    {field}: Mapped[str] = mapped_column(String(255))'
                for field in self.fields
            ]
        )

        content = f"""from sqlalchemy import String
        from sqlalchemy.orm import Mapped, mapped_column
        from app.core.database import Base


        class {self.class_name}(Base):
            __tablename__ = "{self.resource_name}s"

            id: Mapped[int] = mapped_column(primary_key=True, index=True)
        {dynamic_fields}
        """
        self.create_file(
            self.module_path / "models" / f"{self.resource_name}_model.py",
            content,
        )

    def _create_schemas(self):
        dynamic_fields = "\n".join(
            [f"    {field}: str" for field in self.fields]
        )

        content = f"""from pydantic import BaseModel


class {self.class_name}CreateDTO(BaseModel):
{dynamic_fields}


class {self.class_name}ResponseDTO(BaseModel):
    id: int
{dynamic_fields}

    class Config:
        from_attributes = True
"""
        self.create_file(self.module_path / "schemas" / f"{self.resource_name}_dto.py",content)


    def _create_repository(self):
        content = f"""from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.{self.resource_name}.models.{self.resource_name}_model import {self.class_name}


class {self.class_name}Repository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, obj: {self.class_name}):
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def get_all(self):
        result = await self.db.execute(select({self.class_name}))
        return result.scalars().all()

    async def get_by_id(self, obj_id: int):
        result = await self.db.execute(
            select({self.class_name}).where({self.class_name}.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def delete(self, obj):
        await self.db.delete(obj)
        await self.db.commit()
"""
        self.create_file(self.module_path / "repositories" / f"{self.resource_name}_repository.py",content)

    # =========================

    def _create_service(self):
        content = f"""from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.{self.resource_name}.repositories.{self.resource_name}_repository import {self.class_name}Repository
from app.modules.{self.resource_name}.models.{self.resource_name}_model import {self.class_name}


class {self.class_name}Service:

    def __init__(self, db: AsyncSession):
        self.repo = {self.class_name}Repository(db)

    async def create(self, data: dict):
        obj = {self.class_name}(**data)
        return await self.repo.create(obj)

    async def get_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, obj_id: int):
        return await self.repo.get_by_id(obj_id)

    async def delete(self, obj_id: int):
        obj = await self.repo.get_by_id(obj_id)
        if not obj:
            return None
        await self.repo.delete(obj)
        return True
"""
        self.create_file(
            self.module_path / "services" / f"{self.resource_name}_service.py",
            content,
        )

    # =========================

    def _create_controller(self):
        content = f"""from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.{self.resource_name}.services.{self.resource_name}_service import {self.class_name}Service
from app.modules.{self.resource_name}.schemas.{self.resource_name}_dto import {self.class_name}CreateDTO


router = APIRouter(prefix="/{self.resource_name}s", tags=["{self.class_name}"])


@router.post("/")
async def create(
    data: {self.class_name}CreateDTO,
    db: AsyncSession = Depends(get_db),
):
    service = {self.class_name}Service(db)
    return await service.create(data.dict())


@router.get("/")
async def get_all(db: AsyncSession = Depends(get_db)):
    service = {self.class_name}Service(db)
    return await service.get_all()
"""
        self.create_file(
            self.module_path / "controllers" / f"{self.resource_name}_controller.py",
            content,
        )

    # =========================

    def _create_routes(self):
        content = f"""from app.modules.{self.resource_name}.controllers.{self.resource_name}_controller import router
"""
        self.create_file(self.module_path / "routes.py", content)

    # =========================

    def _register_router(self):
        main_path = self.base_path / "app" / "main.py"

        if not main_path.exists():
            return

        self.append_file(
            main_path,
            f"\nfrom app.modules.{self.resource_name}.routes import router as {self.resource_name}_router\napp.include_router({self.resource_name}_router)\n",
        )