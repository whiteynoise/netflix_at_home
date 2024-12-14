"""Create schema

Revision ID: 9293f5989992
Revises: 
Create Date: 2024-12-14 23:01:49.034298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9293f5989992'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS auth;")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF NOT EXISTS auth CASCADE;")
