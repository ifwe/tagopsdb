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
