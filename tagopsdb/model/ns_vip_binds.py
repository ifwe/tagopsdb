from elixir import using_options, belongs_to

from .base import Base


class NsVipBinds(Base):
    using_options(tablename='ns_vip_binds')

    belongs_to(
        'net_default_ip',
        of_kind='NetDefaultIP',
        colname='net_default_ip_id',
        target_column='net_default_ip_id',
        required=True,
        ondelete='cascade'
    )
    belongs_to(
        'app',
        of_kind='Application',
        colname='appID',
        primary_key=True,
        ondelete='cascade',
    )
    belongs_to(
        'vip',
        of_kind='NsVip',
        colname='vipID',
        primary_key=True,
        ondelete='cascade',
    )
    belongs_to(
        'service',
        of_kind='NsService',
        colname='serviceID',
        primary_key=True,
        ondelete='cascade',
    )
    belongs_to(
        'environment',
        of_kind='Environment',
        colname='environmentID',
        primary_key=True,
        ondelete='cascade',
    )
