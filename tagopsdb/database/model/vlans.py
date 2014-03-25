from elixir import Field
from elixir import String, Integer
from elixir import using_options, has_many, belongs_to

from .base import Base


class Vlans(Base):
    using_options(tablename='vlans')
    id = Field(Integer, colname='VlanID', primary_key=True)
    name = Field(String(length=20))
    description = Field(String(length=50))
    # belongs_to(
    #     'environment',
    #     of_kind='Environments',
    #     colname='environmentID',
    #     ondelete='cascade',
    # )
    has_many(
        'subnets',
        of_kind='Subnet',
        # foreign_keys=id
    )
    # # has_many(
    # #     'development_apps',
    # #     of_kind='AppDefinitions',
    # #     colname='Development_VlanID'
    # # )
    # has_many(
    #     'staging_apps',
    #     of_kind='AppDefinitions',
    #     colname='Staging_VlanID'
    # )
    # has_many(
    #     'production_apps',
    #     of_kind='AppDefinitions',
    #     colname='Production_VlanID'
    # )
