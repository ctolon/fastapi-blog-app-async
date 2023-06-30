"""Initialize database with default roles and user."""""
import asyncio

from app import schemas
from app import repo
from app.core.config import settings
from app.db import base  # noqa: F401


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/batuhan/full-stack-fastapi-postgresql/issues/28


async def init_db(
    repo_post = repo.PostRepository
    ) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    
    posts = await repo_post.get_multi()
    if not posts:
        post_in = schemas.PostCreate(
            image_url="example.jpeg",
            title="Hello World",
            content="This is a blog post",
            creator="admin",
        )
            
        post = await repo_post.create(obj_in=post_in)
        
    #return {"status": "OK"}
