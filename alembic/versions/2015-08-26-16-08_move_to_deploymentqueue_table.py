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
    op.create_table(
        'deployment_requests',
        sa.Column('deployment_request_id', sa.Integer, primary_key=True),
        sa.Column('user', sa.String(32), nullable=False),
        sa.Column(
            'status',
            sa.Enum('queued', 'inprogress', 'complete', 'incomplete'),
            server_default='queued',
        ),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.drop_column('deployments', 'user')
    op.drop_column('deployments', 'created_at')
    op.drop_column('deployments', 'dep_type')

    op.add_column(
        'app_deployments',
        sa.Column(
            'deployment_request_id', sa.INTEGER,
            sa.ForeignKey('deployment_requests.deployment_request_id')
        ),
    )
    op.add_column(
        'host_deployments',
        sa.Column(
            'deployment_request_id', sa.INTEGER,
            sa.ForeignKey('deployment_requests.deployment_request_id')
        ),
    )


def downgrade():
    op.add_column(
        'deployments',
        sa.Column('user', sa.String(32), nullable=False)
    )
    op.add_column(
        'deployments',
        sa.Column('declared', sa.DateTime, server_default=sa.func.now()),
    )
    op.add_column(
        'deployments',
        sa.Column('dep_type', sa.Enum('deploy', 'rollback')),
    )

    op.drop_column('app_deployments', 'deployment_request_id')
    op.drop_column('host_deployments', 'deployment_request_id')

    op.drop_table('deployment_requests')
