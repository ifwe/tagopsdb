"""create_vm_info_table

Revision ID: 2dc22680b176
Revises: 33fadda09c4b
Create Date: 2014-08-19 13:39:19.633246

"""

# revision identifiers, used by Alembic.
revision = '2dc22680b176'
down_revision = '33fadda09c4b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'vm_info',
        sa.Column(
            'host_id',
            sa.Integer,
            sa.ForeignKey(
                'hosts.HostID',
                name='fk_vm_info_host_id_hosts',
                ondelete='cascade',
            ),
            primary_key=True,
        ),
        sa.Column('pool', sa.String(10), nullable=False),
        sa.Column('numa_node', sa.Integer, server_default=None),
        mysql_engine='InnoDB',
        mysql_default_charset='utf8',
    )


def downgrade():
    op.drop_table('vm_info')
