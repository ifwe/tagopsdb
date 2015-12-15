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
