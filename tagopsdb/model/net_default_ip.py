from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to, using_table_options
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base


class NetDefaultIP(Base):
    using_options(tablename='net_default_ips')
    using_table_options(
        UniqueConstraint(
            'net_default_id',
            'vlan_id',
            'priority',
            name='ip_key'
        ),
    )

    id = Field(Integer, colname='net_default_ip_id', primary_key=True)
    priority = Field(INTEGER(unsigned=True), required=True)

    belongs_to(
        'net_default',
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
