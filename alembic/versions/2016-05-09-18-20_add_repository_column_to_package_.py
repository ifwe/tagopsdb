"""Add repository column to package_definitions table

Revision ID: 590685167376
Revises: 6c2cecc02f21
Create Date: 2016-05-09 18:20:57.436608

"""

# revision identifiers, used by Alembic.
revision = '590685167376'
down_revision = '6c2cecc02f21'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'package_definitions',
        sa.Column(
            'repository',
            sa.String(length=255),
            nullable=True,
            info={'after': 'path'},
        )
    )


def downgrade():
    op.drop_column('package_definitions', 'repository')
