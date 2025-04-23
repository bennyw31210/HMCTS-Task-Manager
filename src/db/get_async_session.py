from fastapi import Request
from typing import AsyncGenerator

async def get_async_session(REQUEST: Request) -> AsyncGenerator:
    """
    Dependency that provides a SQLAlchemy AsyncSession for a request.

    This function retrieves the `AsyncSession` factory stored in the app state
    and yields a session instance for use in route handlers and services.

    The session is automatically closed after the request is completed.

    Args:
        REQUEST (Request): The current FastAPI request object, which provides
                           access to the application state where the session factory is stored.

    Yields:
        AsyncSession: A SQLAlchemy asynchronous session object.

    Usage:
        Add as a dependency in route handlers using `Depends(get_async_session)`.
    """
    async_session = REQUEST.app.state.ASYNC_SESSION
    async with async_session() as SESSION:
        yield SESSION