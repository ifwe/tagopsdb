from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to

from .base import Base


class Subnet(Base):
    using_options(tablename='subnet')
    id = Field(Integer, colname='SubnetID', primary_key=True)
    ip_address = Field(
        String(length=15),
        colname='ipAddress',
        unique=True
    )
    netmask = Field(String(length=15))
    gateway = Field(String(length=15))

    belongs_to('vlan', of_kind='Vlans', colname='VlanID', ondelete='cascade')
    belongs_to('zone', of_kind='Zones', colname='ZoneID')
