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
