from elixir import Field
from elixir import String, Integer
from elixir import using_options, using_table_options, belongs_to, has_one
from sqlalchemy import UniqueConstraint

from .base import Base


class Ports(Base):
    using_options(tablename='ports')
    using_table_options(
        UniqueConstraint(
            'NetworkID',
            'portNumber',
            name='NetworkID_portNumber'
        ),
    )

    id = Field(Integer, colname='PortID', primary_key=True)
    port_number = Field(String(length=20), colname='portNumber')
    description = Field(String(length=50))
    speed = Field(String(length=20))
    duplex = Field(String(length=20))

    belongs_to(
        'network',
        of_kind='NetworkDevice',
        colname='NetworkID',
        ondelete='cascade',
    )

    has_one(
        'host_interface',
        of_kind='HostInterfaces',
        inverse='port',
    )

    has_one(
        'ilom',
        of_kind='Iloms',
        inverse='port',
    )
