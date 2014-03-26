from elixir import Field
from elixir import String
from elixir import using_options, belongs_to

from .base import Base


class NsServiceParams(Base):
    using_options(tablename='ns_service_params')

    param = Field(String(length=32), primary_key=True)
    value = Field(String(length=128), nullable=False)

    belongs_to(
        'ns_service',
        of_kind='NsService',
        colname='serviceID',
        primary_key=True,
        ondelete='cascade',
    )
