"""fully_use_environment_table_part1

Revision ID: 1bbe1f92e89f
Revises: None
Create Date: 2014-05-22 12:55:32.569767

"""

# revision identifiers, used by Alembic.
revision = '1bbe1f92e89f'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import INTEGER


def upgrade():
    op.add_column(
        'app_deployments',
        sa.Column(
            'environment_id',
            INTEGER(),
            nullable=False,
            info={'after': 'environment'}
        )
    )
    op.execute(
        'update app_deployments join environments using (environment) '
        'set app_deployments.environment_id = environments.environmentID'
    )
    op.create_foreign_key(
        'fk_app_deployments_environment_id_environments',
        'app_deployments',
        'environments',
        ['environment_id'],
        ['environmentID'],
        ondelete='cascade'
    )
    op.add_column(
        'hosts',
        sa.Column(
            'environment_id',
            INTEGER(),
            info={'after': 'environment'}
        )
    )
    op.execute(
        'update hosts join environments using (environment) '
        'set hosts.environment_id = environments.environmentID'
    )
    op.create_foreign_key(
        'fk_hosts_environment_id_environments',
        'hosts',
        'environments',
        ['environment_id'],
        ['environmentID'],
        ondelete='cascade'
    )


def downgrade():
    op.drop_constraint(
        'fk_app_deployments_environment_id_environments',
        'app_deployments',
        type_='foreignkey'
    )
    op.drop_column('app_deployments', 'environment_id')
    op.drop_constraint(
        'fk_hosts_environment_id_environments',
        'hosts',
        type_='foreignkey'
    )
    op.drop_column('hosts', 'environment_id')
