from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to, has_many

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

    has_many(
        'production_apps',
        of_kind='Application',
        inverse='production_vlan'
    )

    has_many(
        'staging_apps',
        of_kind='Application',
        inverse='staging_vlan'
    )

    has_many(
        'development_apps',
        of_kind='Application',
        inverse='development_vlan'
    )

    has_many(
        'subnets',
        of_kind='Subnet',
        inverse='vlan'
    )
