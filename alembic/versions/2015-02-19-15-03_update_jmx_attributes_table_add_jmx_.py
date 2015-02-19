"""update jmx_attributes table add jmx_port column

Revision ID: 3ef044b0a531
Revises: 4113815cf875
Create Date: 2015-02-19 15:03:22.666156

"""

# revision identifiers, used by Alembic.
revision = '3ef044b0a531'
down_revision = '4113815cf875'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import INTEGER


def upgrade():
    op.add_column(
        'jmx_attributes',
        sa.Column(
            'jmx_port',
            INTEGER(unsigned=True, display_width=5),
            nullable=False,
            server_default='9004',
            info={'after': 'attr'}
        )
    )


def downgrade():
    op.drop_column('jmx_attributes', 'jmx_port')
