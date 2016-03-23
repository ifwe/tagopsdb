"""Add deploy_result column to host_deployments table

Revision ID: 251002e30c24
Revises: 9a3ed50ad5f9
Create Date: 2016-03-23 15:01:50.921251

"""

# revision identifiers, used by Alembic.
revision = '251002e30c24'
down_revision = '9a3ed50ad5f9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'host_deployments',
        sa.Column(
            'deploy_result',
            sa.Text,
            info={'after': 'duration'}
        )
    )


def downgrade():
    op.drop_column('host_deployments', 'deploy_result')
