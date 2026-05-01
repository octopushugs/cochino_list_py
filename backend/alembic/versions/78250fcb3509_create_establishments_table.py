"""create establishments table

Revision ID: 78250fcb3509
Revises: 
Create Date: 2026-05-01 14:08:20.296799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78250fcb3509'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.create_table(
    'establishments',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('uuid', sa.UUID, unique=True, nullable=False),
    sa.Column('name', sa.String(1_000), nullable=False),
    sa.Column('permit_name', sa.String(1_000)),
    sa.Column('created_at', sa.DateTime, nullable=False),
    sa.Column('updated_at', sa.DateTime, nullable=False),
    sa.Column('address', sa.String(1_000), nullable=False),
    sa.Column('address2', sa.String(1_000)),
    sa.Column('city', sa.String(1_000), nullable=False),
    sa.Column('state', sa.String(1_000), nullable=False),
    sa.Column('zip', sa.String(10), nullable=False),
  )


def downgrade() -> None:
  op.drop_table('establishments')
