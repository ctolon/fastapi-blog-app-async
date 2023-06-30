from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from app.repo.base import GenericCrudRepository
from app import repo, models

from app.deps.base import get_base_repo


def get_post_repo(base_repo: GenericCrudRepository = Depends(get_base_repo)):
    return repo.PostRepository(model=models.Post, db=base_repo.db)