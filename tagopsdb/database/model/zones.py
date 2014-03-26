from elixir import Field
from elixir import String, Integer
from elixir import using_options

from .base import Base


class Zones(Base):
    using_options(tablename='zones')

    id = Field(Integer, colname='ZoneID', primary_key=True)

    zone_name = Field(String(length=30), colname='zoneName', synonym='name')
    mx_priority = Field(Integer, colname='mxPriority')
    mx_host_id = Field(String(length=30), colname='mxHostID')
    ns_priority = Field(Integer, colname='nsPriority')
    nameserver = Field(String(length=30))
