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

"""create_vm_info_table

Revision ID: 2dc22680b176
Revises: 33fadda09c4b
Create Date: 2014-08-19 13:39:19.633246

"""

# revision identifiers, used by Alembic.
revision = '2dc22680b176'
down_revision = '33fadda09c4b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'vm_info',
        sa.Column(
            'host_id',
            sa.Integer,
            sa.ForeignKey(
                'hosts.HostID',
                name='fk_vm_info_host_id_hosts',
                ondelete='cascade',
            ),
            primary_key=True,
        ),
        sa.Column('pool', sa.String(10), nullable=False),
        sa.Column('numa_node', sa.Integer, server_default=None),
        mysql_engine='InnoDB',
        mysql_default_charset='utf8',
    )


def downgrade():
    op.drop_table('vm_info')
