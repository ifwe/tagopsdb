from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to, using_table_options
from sqlalchemy import UniqueConstraint

from .base import Base


class Cname(Base):
    using_options(tablename='cname')
    using_table_options(
        UniqueConstraint(u'name', u'ZoneID', name=u'name_ZoneID'),
    )
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
