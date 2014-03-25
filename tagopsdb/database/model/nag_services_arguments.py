from elixir import Field, String, belongs_to, using_options
from .base import Base


class NagServicesArguments(Base):
    using_options(tablename='nag_services_arguments')

    value = Field(String(length=120), nullable=False)

    belongs_to(
        'service',
        of_kind='NagServices',
        colname='service_id',
        primary_key=True
    )

    belongs_to(
        'command_argument',
        of_kind='NagCommandArguments',
        colname='command_argument_id',
        primary_key=True
    )
