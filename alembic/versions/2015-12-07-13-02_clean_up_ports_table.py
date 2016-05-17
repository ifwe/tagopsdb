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

"""clean up ports table

Revision ID: 5440c91b2620
Revises: 2ffec29b23fe
Create Date: 2015-12-07 13:02:03.192341

"""

# revision identifiers, used by Alembic.
revision = '5440c91b2620'
down_revision = '2ffec29b23fe'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import VARCHAR

from collections import OrderedDict


ports_columns = OrderedDict([
    ('description', {
        'coltype': VARCHAR(50),
        'after': 'portNumber',
    }),
    ('speed', {
        'coltype': VARCHAR(20),
        'after': 'description',
    }),
    ('duplex', {
        'coltype': VARCHAR(20),
        'after': 'speed',
    }),
])


def upgrade():
    for column in ports_columns.keys():
        op.drop_column('ports', column)


def downgrade():
    for column, params in ports_columns.items():
        nullable = False if 'notnull' in params else True

        op.add_column(
            'ports',
            sa.Column(
                column,
                params['coltype'],
                nullable=nullable,
                info={'after': params['after']}
            )
        )
