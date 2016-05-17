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

"""clean up zones table

Revision ID: 10a5d93ada2d
Revises: 392a60a3851a
Create Date: 2015-12-07 13:16:23.576219

"""

# revision identifiers, used by Alembic.
revision = '10a5d93ada2d'
down_revision = '392a60a3851a'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR

from collections import OrderedDict


zones_columns = OrderedDict([
    ('mxPriority', {
        'coltype': INTEGER(),
        'after': 'zoneName',
    }),
    ('mxHostID', {
        'coltype': VARCHAR(30),
        'after': 'mxPriority',
    }),
    ('nsPriority', {
        'coltype': INTEGER(),
        'after': 'mxHostID',
    }),
    ('nameserver', {
        'coltype': VARCHAR(30),
        'after': 'nsPriority',
    }),
])


def upgrade():
    for column in zones_columns.keys():
        op.drop_column('zones', column)


def downgrade():
    for column, params in zones_columns.items():
        nullable = False if 'notnull' in params else True

        op.add_column(
            'zones',
            sa.Column(
                column,
                params['coltype'],
                nullable=nullable,
                info={'after': params['after']}
            )
        )
