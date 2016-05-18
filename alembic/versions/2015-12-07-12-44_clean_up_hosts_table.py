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

"""clean up hosts table

Revision ID: cf51b447437
Revises: 2ad1b206b6b3
Create Date: 2015-12-07 12:44:13.024217

"""

# revision identifiers, used by Alembic.
revision = 'cf51b447437'
down_revision = '2ad1b206b6b3'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import VARCHAR

from collections import OrderedDict


hosts_columns = OrderedDict([
    ('arch', {
        'coltype': VARCHAR(10),
        'after': 'hostname',
    }),
    ('kernelVersion', {
        'coltype': VARCHAR(20),
        'after': 'arch',
    }),
    ('timezone', {
        'coltype': VARCHAR(10),
        'after': 'distribution',
    }),
    ('powerPort', {
        'coltype': VARCHAR(10),
        'after': 'consolePort',
    }),
    ('powerCircuit', {
        'coltype': VARCHAR(10),
        'after': 'powerPort',
    }),
])


def upgrade():
    for column in hosts_columns.keys():
        op.drop_column('hosts', column)


def downgrade():
    for column, params in hosts_columns.items():
        nullable = False if 'notnull' in params else True

        op.add_column(
            'hosts',
            sa.Column(
                column,
                params['coltype'],
                nullable=nullable,
                info={'after': params['after']}
            )
        )
