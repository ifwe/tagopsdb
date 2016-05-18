# Copyright 2016 Ifwe Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
