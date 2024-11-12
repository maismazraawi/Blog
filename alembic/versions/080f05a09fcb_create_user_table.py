"""create user table

Revision ID: 080f05a09fcb
Revises: 
Create Date: 2024-11-12 12:47:33.095918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '080f05a09fcb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=True),  # initially nullable
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('password', sa.String, nullable=False),
    )


def downgrade() -> None:
    op.alter_column('users', 'name', nullable=False)
