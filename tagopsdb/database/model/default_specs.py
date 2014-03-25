from elixir import Field
from elixir import Integer
from elixir import using_options, belongs_to

from .base import Base


class DefaultSpecs(Base):
    using_options(tablename='default_specs')
    priority = Field(
        Integer,
        nullable=False,
        default=10,
        server_default='10'
    )

    belongs_to(
        'spec',
        of_kind='HostSpecs',
        colname='specID',
        primary_key=True
    )
    belongs_to(
        'app',
        of_kind='AppDefinitions',
        colname='AppID',
        primary_key=True
    )
    belongs_to(
        'environment',
        of_kind='Environments',
        colname='environmentID',
        primary_key=True
    )
