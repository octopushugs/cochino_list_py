"""create closures table

Revision ID: e845338faf5d
Revises: 78250fcb3509
Create Date: 2026-05-01 14:23:00.370434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e845338faf5d'
down_revision: Union[str, Sequence[str], None] = '78250fcb3509'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.create_table(
    'closures',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('uuid', sa.UUID, unique=True, nullable=False),
    sa.Column('establishment_id', sa.Integer, sa.ForeignKey('establishments.id'), nullable=False),
    sa.Column('closed_on', sa.DateTime, nullable=False),
    sa.Column('reopened_on', sa.DateTime, nullable=False),
    sa.Column('reason', sa.String(1_000), nullable=False),
    sa.Column('result', sa.String(255), nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False),
    sa.Column('updated_at', sa.DateTime, nullable=False),
  )


def downgrade() -> None:
  op.drop_table('closures')
