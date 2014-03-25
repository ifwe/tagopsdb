from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to

from .base import Base


class Cname(Base):
    using_options(tablename='cname')
    id = Field(Integer, colname='CnameID', primary_key=True)
    name = Field(String(length=40))

    belongs_to(
        'host',
        of_kind='HostIps',
        colname='IpID',
        onupdate='cascade',
        ondelete='cascade',
    )
    belongs_to(
        'zone',
        of_kind='Zones',
        colname='ZoneID',
        onupdate='cascade',
        ondelete='cascade',
    )
