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

"""Drop GgroupName from jmx_attributes

Revision ID: 8f55a99a7c47
Revises: b4c9f4a3e166
Create Date: 2016-02-08 17:57:52.772411

"""

# revision identifiers, used by Alembic.
revision = '8f55a99a7c47'
down_revision = 'b4c9f4a3e166'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('jmx_attributes', 'GgroupName')


def downgrade():
    op.add_column(
        'jmx_attributes',
        sa.Column(
            'GgroupName',
            sa.String(length=25),
            info={'after': 'jmx_port'},
        )
    )
    # No need to restore data
