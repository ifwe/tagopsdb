from elixir import Field
from elixir import String, Integer
from elixir import using_options, using_table_options, has_many
from sqlalchemy import UniqueConstraint

from .base import Base


class NsDevice(Base):
    using_options(tablename='ns_device')
    using_table_options(
        UniqueConstraint(u'proto', u'host', name=u'proto_host')
    )

    id = Field(Integer, colname='deviceID', primary_key=True)
    proto = Field(String(length=6), required=True)
    host = Field(String(length=32), required=True)

    has_many(
        'vips',
        of_kind='NsVip',
        inverse='device',
    )
