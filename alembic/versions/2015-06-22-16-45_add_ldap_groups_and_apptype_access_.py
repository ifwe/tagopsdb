"""add ldap_groups and apptype_access tables

Revision ID: 3cd9afd76fa5
Revises: 39f9c5d8e06e
Create Date: 2015-06-22 16:45:45.916288

"""

# revision identifiers, used by Alembic.
revision = '3cd9afd76fa5'
down_revision = '39f9c5d8e06e'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT


def upgrade():
    op.create_table(
        'ldap_groups',
        sa.Column(
            'gid',
            INTEGER(unsigned=True),
            primary_key=True,
        ),
        sa.Column('group_name', sa.String(50), nullable=False, unique=True),
        mysql_engine='InnoDB',
        mysql_default_charset='utf8',
    )


    op.create_table(
        'apptype_access',
        sa.Column(
            'environment_id',
            sa.Integer,
            sa.ForeignKey(
                'environments.environmentID',
                name='fk_apptype_access_env_id_env',
                ondelete='cascade',
            ),
            primary_key=True,
        ),
        sa.Column(
            'app_id',
            SMALLINT(),
            sa.ForeignKey(
                'app_definitions.AppID',
                name='fk_apptype_access_app_id_app_def',
                ondelete='cascade',
            ),
            primary_key=True,
        ),
        sa.Column(
            'gid',
            INTEGER(unsigned=True),
            sa.ForeignKey(
                'ldap_groups.gid',
                name='fk_apptype_access_gid_ldap_groups',
                ondelete='cascade',
            ),
            primary_key=True,
        ),
        mysql_engine='InnoDB',
        mysql_default_charset='utf8',
    )


def downgrade():
    op.drop_table('apptype_access')
    op.drop_table('ldap_groups')
