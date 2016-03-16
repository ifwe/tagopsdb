"""Add duration columns to deployment tables

Revision ID: 9a3ed50ad5f9
Revises: 0fe49b5b7f18
Create Date: 2016-03-16 11:28:03.275438

"""

# revision identifiers, used by Alembic.
revision = '9a3ed50ad5f9'
down_revision = '0fe49b5b7f18'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'deployments',
        sa.Column(
            'duration',
            sa.Float,
            nullable=False,
            server_default="0",
            info={'after': 'declared'}
        )
    )

    op.add_column(
        'host_deployments',
        sa.Column(
            'duration',
            sa.Float,
            nullable=False,
            server_default="0",
            info={'after': 'realized'}
        )
    )

    op.add_column(
        'app_deployments',
        sa.Column(
            'duration',
            sa.Float,
            nullable=False,
            server_default="0",
            info={'after': 'realized'}
        )
    )


def downgrade():
    op.drop_column('deployments', 'duration')
    op.drop_column('host_deployments', 'duration')
    op.drop_column('app_deployments', 'duration')
