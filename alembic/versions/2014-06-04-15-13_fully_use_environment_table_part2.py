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

"""fully use environment table part2

Revision ID: 33fadda09c4b
Revises: 1bbe1f92e89f
Create Date: 2014-06-04 15:13:44.069404

"""

# revision identifiers, used by Alembic.
revision = '33fadda09c4b'
down_revision = '1bbe1f92e89f'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import VARCHAR


def upgrade():
    op.drop_column('app_deployments', 'environment')
    op.drop_column('hosts', 'environment')


def downgrade():
    op.add_column(
        'app_deployments',
        sa.Column(
            'environment',
            VARCHAR(length=15),
            nullable=False,
            info={'after': 'status'}
        )
    )
    op.execute(
        'update app_deployments join environments on '
        'app_deployments.environment_id = environments.environmentID '
        'set app_deployments.environment = environments.environment'
    )
    op.add_column(
        'hosts',
        sa.Column(
            'environment',
            VARCHAR(length=15),
            info={'after': 'powerCircuit'}
        )
    )
    op.execute(
        'update hosts join environments on '
        'hosts.environment_id = environments.environmentID '
        'set hosts.environment = environments.environment'
    )
