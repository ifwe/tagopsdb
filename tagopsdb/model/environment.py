from elixir import Field
from elixir import String, Integer
from elixir import using_options, has_many

from .base import Base


class Environment(Base):
    using_options(tablename='environments')

    id = Field(Integer, colname='environmentID', primary_key=True)
    environment = Field(String(length=15), required=True, unique=True)
    env = Field(String(length=12), required=True, unique=True)
    domain = Field(String(length=32), required=True, unique=True)
    prefix = Field(String(length=1), required=True)

    has_many(
        'default_specs',
        of_kind='DefaultSpec',
        inverse='environment'
    )

    has_many(
        'vlans',
        of_kind='Vlan',
        inverse='environment',
    )
