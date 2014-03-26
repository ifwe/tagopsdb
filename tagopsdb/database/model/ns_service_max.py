from elixir import Field
from elixir import using_options, belongs_to
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base


class NsServiceMax(Base):
    using_options(tablename='ns_service_max')

    max_client = Field(
        INTEGER(unsigned=True),
        colname='maxClient',
        nullable=False,
        default=0,
        server_default='0'
    )
    max_requests = Field(
        INTEGER(unsigned=True),
        colname='maxReq',
        nullable=False,
        default=0,
        server_default='0'
    )

    belongs_to(
        'ns_service',
        of_kind='NsService',
        colname='serviceID',
        primary_key=True,
        ondelete='cascade'
    )
    belongs_to(
        'host_spec',
        of_kind='HostSpecs',
        colname='specID',
        primary_key=True,
        ondelete='cascade',
    )
