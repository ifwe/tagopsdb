"""update vlans table name column

Revision ID: 4113815cf875
Revises: f0026976a0c
Create Date: 2015-02-09 16:24:09.040833

"""

# revision identifiers, used by Alembic.
revision = '4113815cf875'
down_revision = 'f0026976a0c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        'vlans',
        'name',
        nullable=False,
        existing_type=sa.String(length=20)
    )
    op.create_unique_constraint('uq_vlans_name', 'vlans', ['name'])


def downgrade():
    # No need to really revert this
    pass
