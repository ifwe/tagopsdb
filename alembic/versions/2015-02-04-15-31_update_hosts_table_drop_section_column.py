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

"""Update hosts table drop section column

Revision ID: f0026976a0c
Revises: 246888f44ad
Create Date: 2015-02-04 15:31:13.353349

"""

# revision identifiers, used by Alembic.
revision = 'f0026976a0c'
down_revision = '246888f44ad'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('hosts', 'section')


def downgrade():
    op.add_column(
        'hosts',
        sa.Column(
            'section',
            sa.String(length=10),
            info={'after': 'cabLocation'}
        )
    )
