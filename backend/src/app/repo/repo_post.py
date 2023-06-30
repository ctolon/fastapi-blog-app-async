from typing import Any, Dict, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repo.base import GenericCrudRepository
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

class PostRepository(GenericCrudRepository[Post, PostCreate, PostUpdate]):
    pass
