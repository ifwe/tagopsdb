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
