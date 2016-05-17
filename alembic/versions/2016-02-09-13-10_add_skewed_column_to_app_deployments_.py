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

"""Add skewed column to app_deployments table

Revision ID: d3a163a2989c
Revises: 627fbd3080bf
Create Date: 2016-02-09 13:10:06.986590

"""

# revision identifiers, used by Alembic.
revision = 'd3a163a2989c'
down_revision = '627fbd3080bf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'app_deployments',
        sa.Column(
            'skewed',
            sa.BOOLEAN(),
            nullable=False,
            server_default='0',
            info={'after': 'realized'},
        )
    )


def downgrade():
    op.drop_column('app_deployments', 'skewed')
