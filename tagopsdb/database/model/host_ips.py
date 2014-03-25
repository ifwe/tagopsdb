from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to

from .base import Base


class HostIps(Base):
    using_options(tablename='host_ips')

    id = Field(Integer, colname='IpID', primary_key=True)
    priority = Field(Integer, nullable=False, default=1, server_default='1')
    a_record = Field(String(length=200), colname='ARecord')
    comments = Field(String(length=200))

    belongs_to('interface', of_kind='HostInterfaces', colname='InterfaceID')
    belongs_to('subnet', of_kind='Subnet', colname='SubnetID')
