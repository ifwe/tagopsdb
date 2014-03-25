from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base


class NsServiceParams(Base):
    using_options(tablename='ns_service_params')

    service_id = Field(
        Integer,
        ForeignKey('ns_service.serviceID'),
        colname='serviceID',
        primary_key=True
    )

    param = Field(String(length=32), primary_key=True)
    value = Field(String(length=128), nullable=False)

    # belongs_to('ns_service', of_kind='NsService', field=service_id)
