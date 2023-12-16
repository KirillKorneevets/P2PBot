import uuid

from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.config.db_config import Base
from sqlalchemy import MetaData

metadata = MetaData()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    username = Column(String, unique=True)
    password = Column(String)

    price_values = relationship("PriceValue", back_populates="user")
    api_tokens = relationship("BitpapaApiTokens", back_populates="user")

class PriceValue(Base):
    __tablename__ = "price_value"

    id = Column(Integer, primary_key=True)
    max_price = Column(Float, default=None)
    min_price = Column(Float, default=None)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    user = relationship("User", back_populates="price_values")

class BitpapaApiTokens(Base):

    __tablename__ = "bitpapa_api_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, nullable=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    api_token = Column(String(100), nullable=True)

    user = relationship("User", back_populates="api_tokens")
