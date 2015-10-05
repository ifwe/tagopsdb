"""Drop package_id from deployments

Revision ID: 1cd4d15cff18
Revises: 2b29596623f7
Create Date: 2015-10-05 14:54:48.975623

"""

# revision identifiers, used by Alembic.
revision = '1cd4d15cff18'
down_revision = '2b29596623f7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('deployments', 'package_id')


def downgrade():
    op.add_column(
        'deployments',
        sa.Column(
            'package_id',
            sa.Integer,
            sa.ForeignKey('packages.package_id', ondelete='cascade'),
            nullable=False,
            info={'after': 'DeploymentID'},
        )
    )

    op.execute(
        'update deployments join host_deployments on '
        'deployments.DeploymentID = host_deployments.DeploymentID '
        'set deployments.package_id = host_deployments.package_id'
    )

    op.execute(
        'update deployments join app_deployments on '
        'deployments.DeploymentID = app_deployments.DeploymentID '
        'set deployments.package_id = app_deployments.package_id'
    )
