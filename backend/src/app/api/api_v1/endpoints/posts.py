from typing import Any, List
import pathlib

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, deps, repo
from app.services.post import PostService
from app.core.media import get_one_media_with_path

router = APIRouter()


@router.post(
    '/',
    response_model=schemas.Post,
    summary="Create new Post"
    )
async def create(
    post_in: schemas.PostCreate,
    repo_post: repo.PostRepository = Depends(deps.get_post_repo),
    ) -> schemas.Post:
    """
    Create new Post.
    """
        
    return await PostService(repo_post).create(obj_in=post_in)


@router.get(
    '/get-all',
    response_model=List[schemas.Post],
    summary="Get all posts"
)
async def get_all(
    *,
    repo_post: repo.PostRepository = Depends(deps.get_post_repo),
    skip: int = 0,
    limit: int = 100,
    ) -> List[schemas.Post]:
    """
    Get all posts.
    """
    
    return await PostService(repo_post).get_all(skip=skip, limit=limit)

@router.get(
    "/{id}",
    response_model=schemas.Post,
    summary="Get a post by id"
)
async def get_post_by_id(
    id: int,
    repo_post: repo.PostRepository = Depends(deps.get_post_repo),
    ) -> schemas.Post:
    """
    Get a specific post by id.
    """
    
    return await PostService(repo_post).get_by_id(id=id)


@router.delete(
    '/{id}',
    response_model=schemas.Post,
    summary="Delete a post"
    )
async def delete(    
    *,
    repo_post: repo.PostRepository = Depends(deps.get_post_repo),
    id: int,
    ):
    """
    Delete a post.
    """
    
    return await PostService(repo_post).remove(id=id)
