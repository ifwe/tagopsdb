from elixir import Field, Integer, using_options, using_table_options
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
        extend_existing=True,
    )

    net_default_id = Field(Integer, primary_key=True)
    vlan_id = Field(Integer, primary_key=True)
