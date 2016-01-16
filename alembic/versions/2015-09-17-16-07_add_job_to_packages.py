"""Add job to packages

Revision ID: 1e725eb01a1f
Revises: 263eeebd28b9
Create Date: 2015-09-17 16:07:52.281084

"""

# revision identifiers, used by Alembic.
revision = '1e725eb01a1f'
down_revision = '263eeebd28b9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'packages',
        sa.Column(
            'job',
            sa.String(length=255),
            nullable=True,
            info={'after': 'revision'},
        )
    )


def downgrade():
    op.drop_column('packages', 'job')
