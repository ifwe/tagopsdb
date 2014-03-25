from elixir import Field
from elixir import String
from elixir import using_options, belongs_to, has_many
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base


class NsVip(Base):
    using_options(tablename='ns_vip')

    id = Field(INTEGER(unsigned=True), colname='vipID', primary_key=True)
    vserver = Field(String(length=64), nullable=False)

    # belongs_to('ns_device', of_kind='NsDevice', colname='deviceID')
    has_many('ns_vip_binds', of_kind='NsVipBinds')
    has_many(
        'app_definitions',
        of_kind='AppDefinitions',
        through='ns_vip_binds',
        via='app_definition'
    )
    has_many(
        'environments',
        of_kind='Environments',
        through='ns_vip_binds',
        via='environment'
    )
    has_many(
        'ns_services',
        of_kind='NsService',
        through='ns_vip_binds',
        via='ns_service'
    )
