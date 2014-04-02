from elixir import using_options, belongs_to

from .base import Base


class NsServiceBinds(Base):
    using_options(tablename='ns_service_binds')

    belongs_to(
        'ns_service',
        of_kind='NsService',
        colname='serviceID',
        primary_key=True,
        ondelete='cascade',
    )
    belongs_to(
        'ns_monitor',
        of_kind='NsMonitor',
        colname='monitorID',
        primary_key=True,
        ondelete='cascade',
    )
