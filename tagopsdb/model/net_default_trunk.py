from elixir import using_options, belongs_to, using_table_options
from sqlalchemy import UniqueConstraint

from .base import Base


class NetDefaultTrunk(Base):
    using_options(tablename='net_default_trunks')
    using_table_options(
        UniqueConstraint(
            'net_default_id',
            'vlan_id',
            name='trunk_key'
        ),
    )

    belongs_to(
        'net_default_id',
        of_kind='NetDefaultMap',
        colname='net_default_id',
        target_column='net_default_id',
        required=True,
        ondelete='cascade'
    )

    belongs_to(
        'vlan',
        of_kind='Vlan',
        colname='vlan_id',
        target_column='VlanID',
        required=True,
        ondelete='cascade'
    )
