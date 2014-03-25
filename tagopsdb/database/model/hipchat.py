from elixir import Field
from elixir import Integer, String
from elixir import using_options

from .base import Base


class Hipchat(Base):
    using_options(tablename='hipchat')

    id = Field(Integer, colname='roomID', primary_key=True)
    room_name = Field(String(length=50), nullable=False, unique=True)
