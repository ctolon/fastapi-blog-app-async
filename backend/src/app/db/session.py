"""Database session management."""""
from typing import Union

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,  async_scoped_session

from contextvars import ContextVar, Token

from app.core.config import settings

session_context: ContextVar[str] = ContextVar("session_context")

def get_session_id() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)

# Create Async db engine and sessions
_postgres_async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    echo=True,
    future=True,
    )

SessionAsyncPostgres = sessionmaker(
    class_= AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    future=True,
    bind=_postgres_async_engine,
    )

session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=SessionAsyncPostgres,
    scopefunc=get_session_id,
)

