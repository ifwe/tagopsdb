from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to

from .base import Base


class HostInterfaces(Base):
    using_options(tablename='host_interfaces')

    id = Field(Integer, colname='InterfaceID', primary_key=True)
    interface_name = Field(String(length=10), colname='interfaceName')
    mac_address = Field(String(length=18), colname='macAddress', unique=True)

    belongs_to('host', of_kind='Hosts', colname='HostID')
    belongs_to('network', of_kind='NetworkDevice', colname='NetworkID')
    belongs_to('port', of_kind='Ports', colname='PortID')
