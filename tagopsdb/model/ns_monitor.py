from elixir import Field
from elixir import Integer, String
from elixir import using_options

from .base import Base


class NsMonitor(Base):
    using_options(tablename='ns_monitor')

    id = Field(Integer, colname='monitorID', primary_key=True)
    monitor = Field(String(length=32), required=True, unique=True)
