from elixir import Field
from elixir import String
from elixir import using_options

from .base import Base


class Locks(Base):
    using_options(tablename='locks')
    val = Field(String(length=64), primary_key=True)
    host = Field(String(length=32), required=True)
