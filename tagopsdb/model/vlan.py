from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to, has_many, \
    has_and_belongs_to_many

from .base import Base


class Vlan(Base):
    using_options(tablename='vlans')
    id = Field(Integer, colname='VlanID', primary_key=True)
    name = Field(String(length=20))
    description = Field(String(length=50))
    belongs_to(
        'environment',
        of_kind='Environment',
        colname='environmentID',
        ondelete='cascade',
    )

    has_many(
        'subnets',
        of_kind='Subnet',
        inverse='vlan'
    )

    has_and_belongs_to_many(
        'net_default',
        of_kind='NetDefaultMap',
        inverse='vlans',
        tablename='net_default_trunks',
        local_colname='vlan_id',
        remote_colname='net_default_id',
        table_kwargs=dict(extend_existing=True),
    )
