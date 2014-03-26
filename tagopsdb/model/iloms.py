from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to

from .base import Base


class Iloms(Base):
    using_options(tablename='iloms')

    id = Field(Integer, colname='ILomID', primary_key=True)
    mac_address = Field(String(length=18), colname='macAddress', unique=True)
    a_record = Field(String(length=200), colname='ARecord')
    comments = Field(String(length=200))

    belongs_to(
        'host',
        of_kind='Hosts',
        colname='HostID',
        ondelete='cascade',
    )

    belongs_to(
        'subnet',
        of_kind='Subnet',
        colname='SubnetID',
        ondelete='cascade',
        required=True
    )

    belongs_to(
        'port',
        of_kind='Ports',
        colname='PortID',
        ondelete='cascade',
    )
