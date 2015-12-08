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
