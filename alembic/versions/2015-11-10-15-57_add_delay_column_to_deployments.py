"""Add delay column to deployments

Revision ID: 13f87d9ec845
Revises: 1cd4d15cff18
Create Date: 2015-11-10 15:57:08.286074

"""

# revision identifiers, used by Alembic.
revision = '13f87d9ec845'
down_revision = '1cd4d15cff18'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'deployments',
        sa.Column(
            'delay',
            sa.Integer,
            info={'after': 'status'},
            server_default=0,
        )
    )


def downgrade():
    op.drop_column('deployments', 'delay')
