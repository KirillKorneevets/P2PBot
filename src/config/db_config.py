from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:Asdcvbjkl763@localhost:5432/P2PBot"

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SyncSession = sessionmaker(engine)

# Dependency
def get_sync_session():
    with SyncSession() as session:
        yield session
