from elixir import Field
from elixir import String
from elixir import using_options, belongs_to, has_many, using_table_options
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base


class NsVip(Base):
    using_options(tablename='ns_vip')
    using_table_options(
        UniqueConstraint(u'deviceID', u'vserver', name=u'device_vserver'),
    )

    id = Field(INTEGER(unsigned=True), colname='vipID', primary_key=True)
    vserver = Field(String(length=64), required=True)

    belongs_to(
        'device',
        of_kind='NsDevice',
        colname='deviceID',
        required=True,
        ondelete='cascade',
    )
    has_many('ns_vip_binds', of_kind='NsVipBinds')
    has_many(
        'app_definitions',
        of_kind='Application',
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
