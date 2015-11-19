"""update hosts table appid null

Revision ID: 41c58f565378
Revises: 263eeebd28b9
Create Date: 2015-11-19 13:39:47.403047

"""

# revision identifiers, used by Alembic.
revision = '41c58f565378'
down_revision = '263eeebd28b9'

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects.mysql import SMALLINT


def upgrade():
    op.alter_column(
        'hosts',
        'AppID',
        nullable=True,
        server_default=None,
        existing_type=SMALLINT(display_width=6)
    )

def downgrade():
    op.alter_column(
        'hosts',
        'AppID',
        nullable=False,
        existing_type=SMALLINT(display_width=6)
    )
