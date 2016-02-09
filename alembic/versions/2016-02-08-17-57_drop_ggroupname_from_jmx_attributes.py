"""Drop GgroupName from jmx_attributes

Revision ID: 8f55a99a7c47
Revises: b4c9f4a3e166
Create Date: 2016-02-08 17:57:52.772411

"""

# revision identifiers, used by Alembic.
revision = '8f55a99a7c47'
down_revision = 'b4c9f4a3e166'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('jmx_attributes', 'GgroupName')


def downgrade():
    op.add_column(
        'jmx_attributes',
        sa.Column(
            'GgroupName',
            sa.String(length=25),
            info={'after': 'jmx_port'},
        )
    )
    # No need to restore data
