
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from app.db.base_class import Base
from app.repo.base import GenericCrudRepository

ModelType = TypeVar("ModelType", bound=Base)
RepoType = TypeVar("RepoType", bound=GenericCrudRepository)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

    
class GenericCrudService(Generic[RepoType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repo: Type[RepoType]):
        """
        Generic Crud Service with default methods to Create, Read, Update, Delete as async (CRUD).

        **Parameters**

        * `repo`: A Repository class which inherits from GenericCrudRepository
        * `schema`: A Pydantic model (schema) class
        """
        self.repo = repo
        
    
    async def get_by_id(self, id: int) -> ModelType:
        return await self.repo.get(id=id)
    
    async def get_all(self, skip: int=0, limit: int = 100) -> List[ModelType]:
        return await self.repo.get_multi(skip=skip, limit=limit)
    
    async def update(self, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]):
        return await self.repo.update(id=id, obj_in=obj_in)
    
    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        return await self.repo.create(obj_in=obj_in)

    async def remove(self, id: int) -> ModelType:
        return await self.repo.remove(id=id)

