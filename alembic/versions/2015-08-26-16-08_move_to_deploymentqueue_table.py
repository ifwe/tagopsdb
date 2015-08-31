"""Move to DeploymentQueue table

Revision ID: 12300441b36c
Revises: 3cd9afd76fa5
Create Date: 2015-08-26 16:08:18.373664

"""

# revision identifiers, used by Alembic.
revision = '12300441b36c'
down_revision = '3cd9afd76fa5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('deployments', 'dep_type')

    op.add_column(
        'deployments',
        sa.Column(
            'status',
            sa.Enum(
                'pending', 'queued', 'inprogress', 'complete', 'failed',
                'canceled', 'stopped',
            ),
            server_default='pending',
            nullable=False,
            info={'after': 'user'},
        ),
    )
    op.execute('update deployments set status="complete"')


def downgrade():
    op.add_column(
        'deployments',
        sa.Column(
            'dep_type',
            sa.Enum('deploy', 'rollback'),
            nullable=False,
            info={'after': 'user'},
        ),
    )
    op.execute('update deployments set dep_type="deploy"')

    op.drop_column('deployments', 'status')
