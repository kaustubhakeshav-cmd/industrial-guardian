from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Create the async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    pool_size=5,
    max_overflow=10
)

# Create a session factory
AsyncSessionLocal = async_sessionmaker(
    engine, 
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    """Dependency injection for database sessions."""
    async with AsyncSessionLocal() as session:
        yield session