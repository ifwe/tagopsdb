from elixir import Field
from elixir import Integer
from elixir import using_options, belongs_to
from sqlalchemy import ForeignKey

from .base import Base


class NsVipBinds(Base):
    using_options(tablename='ns_vip_binds')

    # app_id = Field(Integer, colname='appID', primary_key=True)
    vip_id = Field(
        Integer,
        ForeignKey('ns_vip.vipID'),
        colname='vipID',
        primary_key=True
    )
    service_id = Field(Integer, colname='serviceID', primary_key=True)
    environment_id = Field(Integer, colname='environmentID', primary_key=True)

    # belongs_to('app_definition', of_kind='AppDefinitions', colname='appID')
    belongs_to('ns_vip', of_kind='NsVip', field=vip_id)
    # belongs_to('ns_service', of_kind='NsService', colname='serviceID')
    # belongs_to('environment', of_kind='Environment', colname='environmentID')
