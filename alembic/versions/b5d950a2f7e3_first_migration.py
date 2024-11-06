"""First Migration

Revision ID: b5d950a2f7e3
Revises: 
Create Date: 2024-11-05 15:47:14.772424

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5d950a2f7e3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users" ,
        sa.Column("id", sa.Integer, primary_key= True),
        sa.Column("name", sa.String(20), unique= True, nullable= False),
    )


def downgrade() -> None:
    op.drop_table("users")
