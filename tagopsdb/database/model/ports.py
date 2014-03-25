from elixir import Field
from elixir import String, Integer
from elixir import using_options, has_many, belongs_to

from .base import Base


class Ports(Base):
    using_options(tablename='ports')

    id = Field(Integer, colname='PortID', primary_key=True)
    port_number = Field(String(length=20), colname='portNumber')
    description = Field(String(length=50))
    speed = Field(String(length=20))
    duplex = Field(String(length=20))

    # belongs_to('network', of_kind='NetworkDevice', colname='NetworkID')
    # has_many('host_interfaces', of_kind='HostInterfaces', colname='PortID')
    # has_many('iloms', of_kind='Iloms', colname='PortID')
    # has_many('ilom_subnets', of_kind='Subnets', through='iloms', via='subnet')
    # has_many('ilom_hosts', of_kind='Hosts', through='iloms', via='host')
