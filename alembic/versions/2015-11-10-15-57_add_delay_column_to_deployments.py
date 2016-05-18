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

"""Add delay column to deployments

Revision ID: 13f87d9ec845
Revises: 1cd4d15cff18
Create Date: 2015-11-10 15:57:08.286074

"""

# revision identifiers, used by Alembic.
revision = '13f87d9ec845'
down_revision = '1cd4d15cff18'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'deployments',
        sa.Column(
            'delay',
            sa.Integer,
            info={'after': 'status'},
            server_default='0',
        )
    )


def downgrade():
    op.drop_column('deployments', 'delay')
