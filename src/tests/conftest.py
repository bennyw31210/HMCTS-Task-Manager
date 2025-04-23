import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from db.tables.task import Base
from db.get_async_session import get_async_session

DATABASE_URL = "sqlite+aiosqlite:///:memory:"  # In-memory test DB

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def async_test_engine():
    ENGINE = create_async_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield ENGINE
    await ENGINE.dispose()

@pytest.fixture()
async def async_session(async_test_engine):
    AsyncSessionLocal = sessionmaker(
        bind=async_test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with AsyncSessionLocal() as session:
        yield session

@pytest.fixture()
async def CLIENT(async_session):
    # Dependency override
    app.dependency_overrides[get_async_session] = lambda: async_session

    # Use ASGITransport to allow AsyncClient to talk directly to the FastAPI app
    TRANSPORT = ASGITransport(app=app)

    async with AsyncClient(transport=TRANSPORT, base_url="http://testserver") as c:
        yield c