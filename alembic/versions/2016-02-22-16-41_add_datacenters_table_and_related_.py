"""Add datacenters table and related changes

Revision ID: 0fe49b5b7f18
Revises: d3a163a2989c
Create Date: 2016-02-22 16:41:48.518927

"""

# revision identifiers, used by Alembic.
revision = '0fe49b5b7f18'
down_revision = 'd3a163a2989c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    datacenters_table = op.create_table(
        'datacenters',
        sa.Column('dc_id', sa.Integer, primary_key=True),
        sa.Column('dc_name', sa.String(length=32), unique=True,
                  nullable=False),
        sa.Column('physical_location', sa.String(length=64), nullable=False),
        sa.Column('priority', sa.Integer, nullable=False),
        mysql_engine='InnoDB'
    )

    op.bulk_insert(
        datacenters_table,
        [
            {
                'dc_name': 'sf_drt_1',
                'physical_location': '365 Main St, San Francisco, CA',
                'priority': 10,
            }
        ]
    )

    conn = op.get_bind()
    result = conn.execute(datacenters_table.select())
    dc_id = str(result.first()['dc_id'])

    op.add_column(
        'hosts',
        sa.Column(
            'dc_id',
            sa.Integer,
            sa.ForeignKey(
                'datacenters.dc_id',
                name='fk_hosts_dc_id_datacenters',
                ondelete='cascade'
            ),
            nullable=True,
            server_default=dc_id,
            info={'after': 'AppID'},
        )
    )

    op.execute(
        'update hosts join datacenters on hosts.dc_id = datacenters.dc_id '
        'set hosts.dc_id = datacenters.dc_id'
    )

    op.alter_column(
        'hosts',
        'dc_id',
        nullable=False,
        existing_type=sa.Integer,
    )

    op.add_column(
        'net_default_maps',
        sa.Column(
            'dc_id',
            sa.Integer,
            sa.ForeignKey(
                'datacenters.dc_id',
                name='fk_net_default_maps_dc_id_datacenters',
                ondelete='cascade'
            ),
            nullable=True,
            server_default=dc_id,
            info={'after': 'net_default_id'},
        )
    )

    op.execute(
        'update net_default_maps join datacenters '
        'on net_default_maps.dc_id = datacenters.dc_id '
        'set net_default_maps.dc_id = datacenters.dc_id'
    )

    op.alter_column(
        'net_default_maps',
        'dc_id',
        nullable=False,
        existing_type=sa.Integer,
    )


def downgrade():
    op.drop_constraint(
        'fk_hosts_dc_id_datacenters',
        'hosts',
        type_='foreignkey'
    )
    op.drop_column('hosts', 'dc_id')
    op.drop_constraint(
        'fk_net_default_maps_dc_id_datacenters',
        'net_default_maps',
        type_='foreignkey'
    )
    op.drop_column('net_default_maps', 'dc_id')
    op.drop_table('datacenters')
