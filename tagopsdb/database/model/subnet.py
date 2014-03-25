from elixir import Field
from elixir import String, Integer
from elixir import using_options, has_many, belongs_to

from sqlalchemy import ForeignKey

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

    belongs_to('vlan', of_kind='Vlans', colname='VlanID')
    belongs_to('zone', of_kind='Zones', colname='ZoneID')

    # has_many('hosts', of_kind='HostIps', colname='SubnetID')
    # has_many(
    #     'host_interfaces',
    #     of_kind='HostInterfaces',
    #     through='hosts',
    #     via='host_interfaces'
    # )

    # has_many('iloms', of_kind='Iloms', colname='SubnetID')
    # has_many('ilom_hosts', of_kind='Hosts', through='iloms', via='host')
    # has_many('ilom_ports', of_kind='Ports', through='iloms', via='port')
