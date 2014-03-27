from elixir import Field
from elixir import String, Integer, Boolean, Enum
from elixir import using_options, has_many
from sqlalchemy.dialects.mysql import SMALLINT, INTEGER, MEDIUMTEXT

from .base import Base


class HostSpec(Base):
    using_options(tablename='host_specs')

    id = Field(Integer, colname='specID', primary_key=True)
    gen = Field(String(length=4))
    memory_size = Field(Integer, colname='memorySize')
    cores = Field(SMALLINT(display_width=2), required=True)
    cpu_speed = Field(INTEGER(display_width=6), colname='cpuSpeed')
    disk_size = Field(INTEGER(display_width=6), colname='diskSize')
    vendor = Field(String(length=20))
    model = Field(String(length=20))
    control = Field(Enum(u'digi', u'ipmi', u'libvirt', u'vmware'))
    virtual = Field(Boolean, required=True, default=0, server_default='0')
    expansions = Field(MEDIUMTEXT())

    has_many(
        'defaults',
        of_kind="DefaultSpec",
        inverse='spec'
    )

    has_many(
        'hosts',
        of_kind='Hosts',
        inverse='spec',
    )
