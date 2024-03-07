import uuid

from sqlalchemy import Column, String, Integer, Float, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.config.db_config import AsyncBase
from sqlalchemy import MetaData

metadata = MetaData()

class BitpapaApiTokens(AsyncBase):

    __tablename__ = "bitpapa_api_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    api_token = Column(String(100), nullable=True)

    __table_args__ = (
        UniqueConstraint('user_id', name='uq_user_id'),
    )


    user = relationship("User", back_populates="api_tokens")

class User(AsyncBase):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    is_bot_active = Column(Boolean, default=False)

    price_values = relationship("PriceValueBYN", back_populates="user")
    api_tokens = relationship("BitpapaApiTokens", back_populates="user")
    bitpapa_user_name = relationship("BitpapaUserName", back_populates="user")



class PriceValueBYN(AsyncBase):
    __tablename__ = "price_value_byn"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    is_erip_sell_active = Column(Boolean, default=False)
    erip_sell = Column(Float, default=None)

    is_erip_buy_active = Column(Boolean, default=False)
    erip_buy = Column(Float, default=None)

    is_card2card_sell_active = Column(Boolean, default=False)
    card2card_sell = Column(Float, default=None)

    is_card2card_buy_active = Column(Boolean, default=False)
    card2card_buy = Column(Float, default=None)

    is_alfabank_sell_active = Column(Boolean, default=False)
    alfabank_sell = Column(Float, default=None)

    is_alfabank_buy_active = Column(Boolean, default=False)
    alfabank_buy = Column(Float, default=None)

    user = relationship("User", back_populates="price_values")


class BitpapaUserName(AsyncBase):
    __tablename__ = "bitpapa_user_name"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    username = Column(String, unique=True)

    user = relationship("User", back_populates="bitpapa_user_name")