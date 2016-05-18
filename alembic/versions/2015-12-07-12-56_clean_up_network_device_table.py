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

"""clean up network_device table

Revision ID: 2ffec29b23fe
Revises: cf51b447437
Create Date: 2015-12-07 12:56:24.158721

"""

# revision identifiers, used by Alembic.
revision = '2ffec29b23fe'
down_revision = 'cf51b447437'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import VARCHAR

from collections import OrderedDict


network_device_columns = OrderedDict([
    ('model', {
        'coltype': VARCHAR(50),
        'after': 'systemName',
    }),
    ('hardwareCode', {
        'coltype': VARCHAR(20),
        'after': 'model',
    }),
    ('softwareCode', {
        'coltype': VARCHAR(20),
        'after': 'hardwareCode',
    }),
])


def upgrade():
    for column in network_device_columns.keys():
        op.drop_column('networkDevice', column)


def downgrade():
    for column, params in network_device_columns.items():
        nullable = False if 'notnull' in params else True

        op.add_column(
            'networkDevice',
            sa.Column(
                column,
                params['coltype'],
                nullable=nullable,
                info={'after': params['after']}
            )
        )
