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

"""Add job to packages

Revision ID: 1e725eb01a1f
Revises: 263eeebd28b9
Create Date: 2015-09-17 16:07:52.281084

"""

# revision identifiers, used by Alembic.
revision = '1e725eb01a1f'
down_revision = '263eeebd28b9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'packages',
        sa.Column(
            'job',
            sa.String(length=255),
            nullable=True,
            info={'after': 'revision'},
        )
    )


def downgrade():
    op.drop_column('packages', 'job')
