from elixir import Field
from elixir import Integer
from elixir import using_options, belongs_to

from .base import Base


class DefaultSpec(Base):
    using_options(tablename='default_specs')
    priority = Field(
        Integer,
        required=True,
        default=10,
        server_default='10'
    )

    belongs_to(
        'spec',
        of_kind='HostSpecs',
        colname='specID',
        ondelete='cascade',
        primary_key=True
    )
    belongs_to(
        'app',
        of_kind='Application',
        colname='AppID',
        ondelete='cascade',
        primary_key=True
    )
    belongs_to(
        'environment',
        of_kind='Environments',
        colname='environmentID',
        ondelete='cascade',
        primary_key=True
    )
