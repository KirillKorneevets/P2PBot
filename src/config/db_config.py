from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:Asdcvbjkl763@localhost:5432/P2PBot"

async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncBase = declarative_base()
async_Session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# Dependency
async def get_async_session():
    async with async_Session() as session:
        yield session