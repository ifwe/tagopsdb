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

"""clean up service_event table

Revision ID: 392a60a3851a
Revises: 5440c91b2620
Create Date: 2015-12-07 13:07:56.356627

"""

# revision identifiers, used by Alembic.
revision = '392a60a3851a'
down_revision = '5440c91b2620'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import VARCHAR

from collections import OrderedDict


service_event_columns = OrderedDict([
    ('user', {
        'coltype': VARCHAR(20),
        'after': 'HostID',
    }),
    ('powerStatus', {
        'coltype': VARCHAR(10),
        'after': 'serviceStatus',
    }),
    ('vendorTicket', {
        'coltype': VARCHAR(20),
        'after': 'powerStatus',
    }),
])


def upgrade():
    for column in service_event_columns.keys():
        op.drop_column('serviceEvent', column)


def downgrade():
    for column, params in service_event_columns.items():
        nullable = False if 'notnull' in params else True

        op.add_column(
            'serviceEvent',
            sa.Column(
                column,
                params['coltype'],
                nullable=nullable,
                info={'after': params['after']}
            )
        )
