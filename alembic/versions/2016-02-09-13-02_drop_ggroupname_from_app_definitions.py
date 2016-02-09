"""Drop GgroupName from app_definitions

Revision ID: 627fbd3080bf
Revises: 8f55a99a7c47
Create Date: 2016-02-09 13:02:05.377505

"""

# revision identifiers, used by Alembic.
revision = '627fbd3080bf'
down_revision = '8f55a99a7c47'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('app_definitions', 'GgroupName')


def downgrade():
    op.add_column(
        'app_definitions',
        sa.Column(
            'GgroupName',
            sa.String(length=25),
            info={'after': 'GangliaID'},
        )
    )
    # No need to restore data
