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

"""clean up asset table

Revision ID: 2ad1b206b6b3
Revises: 41c58f565378
Create Date: 2015-12-04 16:21:42.397740

"""

# revision identifiers, used by Alembic.
revision = '2ad1b206b6b3'
down_revision = '41c58f565378'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import DATE, VARCHAR

from collections import OrderedDict


asset_columns = OrderedDict([
    ('dateReceived', {
        'coltype': DATE,
        'after': 'HostID',
    }),
    ('description', {
        'coltype': VARCHAR(20),
        'after': 'dateReceived',
    }),
    ('invoiceNumber', {
        'coltype': VARCHAR(20),
        'after': 'taggedSerial',
    }),
    ('locationSite', {
        'coltype': VARCHAR(20),
        'after': 'invoiceNumber',
    }),
    ('locationOwner', {
        'coltype': VARCHAR(20),
        'after': 'locationSite',
    }),
    ('costPerItem', {
        'coltype': VARCHAR(20),
        'after': 'locationOwner',
    }),
    ('dateOfInvoice', {
        'coltype': DATE,
        'after': 'costPerItem',
    }),
    ('warrantyStart', {
        'coltype': DATE,
        'after': 'dateOfInvoice',
    }),
    ('warrantyEnd', {
        'coltype': DATE,
        'after': 'warrantyStart',
    }),
    ('warrantyLevel', {
        'coltype': VARCHAR(20),
        'after': 'warrantyEnd',
    }),
    ('warrantyID', {
        'coltype': VARCHAR(20),
        'after': 'warrantyLevel',
    }),
    ('vendorContact', {
        'coltype': VARCHAR(20),
        'after': 'warrantyID',
    }),
])


def upgrade():
    for column in asset_columns.keys():
        op.drop_column('asset', column)


def downgrade():
    for column, params in asset_columns.items():
        nullable = False if 'notnull' in params else True

        op.add_column(
            'asset',
            sa.Column(
                column,
                params['coltype'],
                nullable=nullable,
                info={'after': params['after']}
            )
        )
