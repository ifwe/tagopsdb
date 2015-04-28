"""update app definitions table distribution column

Revision ID: 39f9c5d8e06e
Revises: 3ef044b0a531
Create Date: 2015-04-28 11:40:19.975553

"""

# revision identifiers, used by Alembic.
revision = '39f9c5d8e06e'
down_revision = '3ef044b0a531'

from alembic import op
import sqlalchemy as sa

new_type = sa.Enum(
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
    u'ontap'
)
old_type = sa.Enum(
    u'centos5.4',
    u'centos6.2',
    u'centos6.4',
    u'centos6.5',
    u'centos7.0',
    u'fedora18',
    u'rhel5.3',
    u'rhel6.2',
    u'rhel6.3',
    u'rhel6.4',
    u'rhel6.5',
    u'ontap'
)


def upgrade():
    op.alter_column(
        'app_definitions',
        'distribution',
        nullable=False,
        type_=new_type,
        existing_type=old_type
    )


def downgrade():
    op.alter_column(
        'app_definitions',
        'distribution',
        nullable=False,
        type_=old_type,
        existing_type=new_type
    )
