from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to

from .base import Base


class Vlans(Base):
    using_options(tablename='vlans')
    id = Field(Integer, colname='VlanID', primary_key=True)
    name = Field(String(length=20))
    description = Field(String(length=50))
    belongs_to(
        'environment',
        of_kind='Environments',
        colname='environmentID',
        ondelete='cascade',
    )
