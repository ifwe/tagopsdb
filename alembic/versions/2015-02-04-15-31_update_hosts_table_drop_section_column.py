"""Update hosts table drop section column

Revision ID: f0026976a0c
Revises: 246888f44ad
Create Date: 2015-02-04 15:31:13.353349

"""

# revision identifiers, used by Alembic.
revision = 'f0026976a0c'
down_revision = '246888f44ad'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('hosts', 'section')


def downgrade():
    op.add_column(
        'hosts',
        sa.Column(
            'section',
            sa.String(length=10),
            info={'after': 'cabLocation'}
        )
    )
