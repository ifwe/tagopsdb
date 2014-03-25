from elixir import Field
from elixir import Integer, String
from elixir import using_options

from .base import Base


class Ganglia(Base):
    using_options(tablename='ganglia')

    id = Field(Integer, colname='GangliaID', primary_key=True)
    cluster_name = Field(String(length=50))
    port = Field(
        Integer,
        nullable=False,
        default='8649',
        server_default='8649'
    )
