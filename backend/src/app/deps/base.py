"""API Dependencies Module."""
from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.repo.base import GenericCrudRepository
from app.db.session import SessionAsyncPostgres
from app.db.base_class import Base


async def get_db() -> Generator:      
    try:
        db = SessionAsyncPostgres()
        yield db
    except:
        await db.rollback()
        raise
    finally:
        await db.close()
        
async def get_base_repo(db: AsyncSession = Depends(get_db)):
    return GenericCrudRepository(model=Base, db=db)
