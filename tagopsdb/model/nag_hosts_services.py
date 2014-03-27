from elixir import using_options, belongs_to
from .base import Base


class NagHostsServices(Base):
    using_options(tablename='nag_hosts_services')

    belongs_to(
        'host',
        of_kind='Hosts',
        colname='host_id',
        primary_key=True,
        ondelete='cascade',
    )
    belongs_to(
        'service',
        of_kind='NagServices',
        colname='service_id',
        primary_key=True,
        ondelete='cascade',
    )
    belongs_to(
        'server_app',
        of_kind='Application',
        colname='server_app_id',
        primary_key=True
    )
