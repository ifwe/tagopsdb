from .base import Base

from elixir import using_options, belongs_to


class NagApptypesServices(Base):
    using_options(tablename='nag_apptypes_services')

    belongs_to(
        'app',
        of_kind='AppDefinitions',
        colname='app_id',
        primary_key=True,
        ondelete='cascade'
    )
    belongs_to(
        'service',
        of_kind='NagServices',
        colname='service_id',
        primary_key=True,
        ondelete='cascade'
    )
    belongs_to(
        'server_app',
        of_kind='AppDefinitions',
        colname='server_app_id',
        primary_key=True
    )
    belongs_to(
        'environment',
        of_kind='Environments',
        colname='environment_id',
        primary_key=True,
        ondelete='cascade'
    )
