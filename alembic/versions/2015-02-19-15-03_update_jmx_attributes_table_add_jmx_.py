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

"""update jmx_attributes table add jmx_port column

Revision ID: 3ef044b0a531
Revises: 4113815cf875
Create Date: 2015-02-19 15:03:22.666156

"""

# revision identifiers, used by Alembic.
revision = '3ef044b0a531'
down_revision = '4113815cf875'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import INTEGER


def upgrade():
    op.add_column(
        'jmx_attributes',
        sa.Column(
            'jmx_port',
            INTEGER(unsigned=True, display_width=5),
            nullable=False,
            server_default='9004',
            info={'after': 'attr'}
        )
    )


def downgrade():
    op.drop_column('jmx_attributes', 'jmx_port')
