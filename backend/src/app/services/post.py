
from typing import Any, List, Type
import pathlib

from fastapi import Depends, HTTPException

from app import models, schemas
from app.repo.repo_post import PostRepository
from app.services.base import GenericCrudService
from app.core.media import get_one_media_with_path

        
class PostService(GenericCrudService):
    def __init__(self, repo: PostRepository):
        self.repo = repo
        
    async def create(self, obj_in: schemas.PostCreate) -> models.Post:
        
        # transaction
        if "." in obj_in.image_url:
            image = await get_one_media_with_path(obj_in.image_url)
            if image is None:
                raise HTTPException(status_code=404, detail=f"Image not found with name: {obj_in.image_url}")
        else:
            raise HTTPException(status_code=422, detail=f"You must provide a valid image file name. You provided: {obj_in.image_url}")
        
        return await self.repo.create(obj_in=obj_in)

        
