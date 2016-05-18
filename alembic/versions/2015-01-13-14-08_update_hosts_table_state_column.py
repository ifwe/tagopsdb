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

"""update hosts table state column

Revision ID: 246888f44ad
Revises: 46d842a18450
Create Date: 2015-01-13 14:08:46.371508

"""

# revision identifiers, used by Alembic.
revision = '246888f44ad'
down_revision = '46d842a18450'

from alembic import op
import sqlalchemy as sa

new_type = sa.Enum(
    u'baremetal',
    u'operational',
    u'repair',
    u'parts',
    u'reserved',
    u'escrow',
    u'sold'
)
old_type = sa.Enum(
    u'baremetal',
    u'operational',
    u'repair',
    u'parts',
    u'reserved',
    u'escrow'
)


def upgrade():
    op.alter_column(
        'hosts',
        'state',
        nullable=False,
        type_=new_type,
        existing_type=old_type
    )


def downgrade():
    op.alter_column(
        'hosts',
        'state',
        nullable=False,
        type_=old_type,
        existing_type=new_type
    )
