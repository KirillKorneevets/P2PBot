"""empty message

Revision ID: b1214375fb6f
Revises: 91d3aa19df16
Create Date: 2024-01-30 15:05:24.215711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1214375fb6f'
down_revision: Union[str, None] = '91d3aa19df16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('price_value_byn', sa.Column('is_erip_sell_active', sa.Boolean(), nullable=True))
    op.add_column('price_value_byn', sa.Column('is_erip_buy_active', sa.Boolean(), nullable=True))
    op.add_column('price_value_byn', sa.Column('is_card2card_sell_active', sa.Boolean(), nullable=True))
    op.add_column('price_value_byn', sa.Column('is_card2card_buy_active', sa.Boolean(), nullable=True))
    op.add_column('price_value_byn', sa.Column('is_alfabank_sell_active', sa.Boolean(), nullable=True))
    op.add_column('price_value_byn', sa.Column('is_alfabank_buy_active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('price_value_byn', 'is_alfabank_buy_active')
    op.drop_column('price_value_byn', 'is_alfabank_sell_active')
    op.drop_column('price_value_byn', 'is_card2card_buy_active')
    op.drop_column('price_value_byn', 'is_card2card_sell_active')
    op.drop_column('price_value_byn', 'is_erip_buy_active')
    op.drop_column('price_value_byn', 'is_erip_sell_active')
    # ### end Alembic commands ###
