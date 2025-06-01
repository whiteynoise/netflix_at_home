# flake8: noqa
"""roles

Revision ID: ce53ce659f8d
Revises: cd2229851cde
Create Date: 2025-05-29 21:17:11.359274

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'ce53ce659f8d'
down_revision: Union[str, None] = 'cd2229851cde'
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
