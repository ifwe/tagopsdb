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

"""Add repository column to package_definitions table

Revision ID: 590685167376
Revises: 6c2cecc02f21
Create Date: 2016-05-09 18:20:57.436608

"""

# revision identifiers, used by Alembic.
revision = '590685167376'
down_revision = '6c2cecc02f21'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'package_definitions',
        sa.Column(
            'repository',
            sa.String(length=255),
            nullable=True,
            info={'after': 'path'},
        )
    )


def downgrade():
    op.drop_column('package_definitions', 'repository')
