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
