from elixir import Field
from elixir import String, Integer
from elixir import using_options, has_many

from .base import Base


class Zone(Base):
    using_options(tablename='zones')

    id = Field(Integer, colname='ZoneID', primary_key=True)

    zone = Field(String(length=30), colname='zoneName', synonym='name')
    mx_priority = Field(Integer, colname='mxPriority')
    mx_host_id = Field(String(length=30), colname='mxHostID')
    ns_priority = Field(Integer, colname='nsPriority')
    nameserver = Field(String(length=30))

    has_many(
        'cnames',
        of_kind='Cname',
        inverse='zone'
    )

    has_many(
        'subnets',
        of_kind='Subnet',
        inverse='zone'
    )