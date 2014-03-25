from elixir import Field
from elixir import Integer
from elixir import using_options, belongs_to
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base


class NsServiceMax(Base):
    using_options(tablename='ns_service_max')

    spec_id = Field(
        Integer,
        ForeignKey('host_specs.specID'),
        colname='specID',
        primary_key=True
    )
    service_id = Field(
        Integer,
        ForeignKey('ns_service.serviceID'),
        colname='serviceID',
        primary_key=True
    )
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

    # belongs_to('ns_service', of_kind='NsService', field=service_id)
    # belongs_to('host_spec', of_kind='HostSpecs', field=spec_id)
