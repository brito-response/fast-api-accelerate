def base_repository_template() -> str:
    return """
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Type, TypeVar, Generic, List, Optional

T = TypeVar("T")

class BaseRepository(Generic[T]):

    def __init__(self, model: Type[T], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_all(self) -> List[T]:
        result = await self.db.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, id: int) -> Optional[T]:
        result = await self.db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def get_by_field(self, field_name: str, value):
        field = getattr(self.model, field_name, None)

        if not field:
            raise AttributeError(f"{self.model.__name__} has no field '{field_name}'")

        result = await self.db.execute(select(self.model).filter(field == value))
        return result.scalars().first()

    async def create(self, entity: T) -> T:
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity
    
    async def delete(self, id: int) -> bool:
        entity = await self.get_by_id(id)
        if not entity:
            return False
        await self.db.delete(entity)
        await self.db.commit()
        return True
    
    async def update(self, entity: T) -> T:
        await self.db.commit()
        await self.db.refresh(entity)
        return entity
"""