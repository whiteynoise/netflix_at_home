"""create_schema

Revision ID: fbd944cbcb63
Revises:
Create Date: 2024-12-16 19:41:47.190303

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fbd944cbcb63"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS auth;")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF NOT EXISTS auth CASCADE;")
