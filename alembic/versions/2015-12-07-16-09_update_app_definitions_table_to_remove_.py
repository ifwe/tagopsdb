"""update app definitions table to remove enum for distribution

Revision ID: 10aa1611b456
Revises: 10a5d93ada2d
Create Date: 2015-12-07 16:09:11.198670

"""

# revision identifiers, used by Alembic.
revision = '10aa1611b456'
down_revision = '10a5d93ada2d'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import VARCHAR


orig_type = sa.Enum(
    u'centos5.4',
    u'centos6.2',
    u'centos6.4',
    u'centos6.5',
    u'centos7.0',
    u'centos7.1',
    u'fedora18',
    u'rhel5.3',
    u'rhel6.2',
    u'rhel6.3',
    u'rhel6.4',
    u'rhel6.5',
    u'ontap',
    u'windows'
)


def upgrade():
    op.alter_column(
        'app_definitions',
        'distribution',
        nullable=False,
        type_=VARCHAR(20)
    )


def downgrade():
    # Having issues getting the downgrade to work right with
    # respect to the nullable setting (should not be NULL),
    # disallowing downgrade
    # pass

    op.alter_column(
        'app_definitions',
        'distribution',
        nullable=False,
        type_=orig_type
    )
