"""add UniqueConstraint bitpapa_api_tokens

Revision ID: 359fa469d1fb
Revises: 0617e5b5454b
Create Date: 2024-01-19 14:24:57.479854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '359fa469d1fb'
down_revision: Union[str, None] = '0617e5b5454b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint('uq_bitpapa_api_tokens', 'bitpapa_api_tokens', ['api_token'])


def downgrade() -> None:
    pass
