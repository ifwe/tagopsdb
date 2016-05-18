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

"""Add git commit hash to packages table

Revision ID: 6c2cecc02f21
Revises: 251002e30c24
Create Date: 2016-03-26 15:55:29.035807

"""

# revision identifiers, used by Alembic.
revision = '6c2cecc02f21'
down_revision = '251002e30c24'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'packages',
        sa.Column(
            'commit_hash',
            sa.String(length=40),
            nullable=True,
            info={'after': 'job'},
        )
    )


def downgrade():
    op.drop_column('packages', 'commit_hash')
