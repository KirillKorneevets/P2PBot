from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"postgresql+asyncpg://postgres:Asdcvbjkl763@localhost:5432/P2PBot"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
