"""update app and host deployment tables state column

Revision ID: 263eeebd28b9
Revises: 12300441b36c
Create Date: 2015-09-03 14:45:11.463435

"""

# revision identifiers, used by Alembic.
revision = '263eeebd28b9'
down_revision = '12300441b36c'

from alembic import op
import sqlalchemy as sa


app_new_type = sa.Enum(
    u'complete',
    u'incomplete',
    u'inprogress',
    u'invalidated',
    u'pending',
    u'validated',
)
app_old_type = sa.Enum(
    u'complete',
    u'incomplete',
    u'inprogress',
    u'invalidated',
    u'validated',
)
host_new_type = sa.Enum(
    u'failed',
    u'inprogress',
    u'ok',
    u'pending',
)
host_old_type = sa.Enum(
    u'inprogress',
    u'failed',
    u'ok',
)


def upgrade():
    op.alter_column(
        'app_deployments',
        'status',
        nullable=False,
        type_=app_new_type,
        existing_type=app_old_type
    )
    op.alter_column(
        'host_deployments',
        'status',
        nullable=False,
        type_=host_new_type,
        existing_type=host_old_type
    )


def downgrade():
    op.alter_column(
        'app_deployments',
        'status',
        nullable=False,
        type_=app_old_type,
        existing_type=app_new_type
    )
    op.alter_column(
        'host_deployments',
        'status',
        nullable=False,
        type_=host_old_type,
        existing_type=host_new_type
    )
