def base_service_template() -> str:
    return """
from typing import Generic, TypeVar, List
from fastapi import HTTPException, status

T = TypeVar("T")

class BaseService(Generic[T]):

    def __init__(self, repository):
        self.repository = repository

    async def get_all(self) -> List[T]:
        return await self.repository.get_all()

    async def get_by_id(self, id: int) -> T:
        entity = await self.repository.get_by_id(id)
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"entity with this id {id} not found")
        return entity
"""