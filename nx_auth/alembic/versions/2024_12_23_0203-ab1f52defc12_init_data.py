"""create_schema

Revision ID: ab1f52defc12
Revises: 640723fda243
Create Date: 2024-12-23 02:03:14.160565

"""

from typing import Sequence, Union
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "ab1f52defc12"
down_revision: str = "640723fda243"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO auth.roles (role_id, title)
        VALUES
            ('3fc6cea2-cdc0-406d-9695-aa59dab90a95', 'admin'),
            ('dc24961a-fb3e-4bba-ba48-db71a9ae5582', 'base_user'),
            ('b7a62450-3508-4763-ad1e-7feca9899d40', 'sub_user');
    """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM auth.roles where title in ('admin', 'base_user', 'sub_user');
    """
    )
