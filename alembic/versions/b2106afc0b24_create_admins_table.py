"""create admins table

Revision ID: b2106afc0b24
Revises: b5d950a2f7e3
Create Date: 2024-11-06 14:04:14.333419

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2106afc0b24'
down_revision: Union[str, None] = 'b5d950a2f7e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "admins",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(length=20), unique= True, nullable= False),
        sa.Column("users_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    )


def downgrade() -> None:
    op.drop_table("admins")
