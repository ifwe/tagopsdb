from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to, using_table_options
from sqlalchemy import UniqueConstraint

from .base import Base


class HostInterfaces(Base):
    using_options(tablename='host_interfaces')
    using_table_options(
        UniqueConstraint(u'HostID', u'interfaceName')
    )

    id = Field(Integer, colname='InterfaceID', primary_key=True)
    interface_name = Field(String(length=10), colname='interfaceName')
    mac_address = Field(String(length=18), colname='macAddress', unique=True)

    belongs_to(
        'host',
        of_kind='Hosts',
        colname='HostID',
        ondelete='cascade',
    )
    belongs_to(
        'network',
        of_kind='NetworkDevice',
        colname='NetworkID',
        ondelete='cascade',
    )
    belongs_to(
        'port',
        of_kind='Ports',
        colname='PortID',
        ondelete='cascade',
    )
