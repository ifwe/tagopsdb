from elixir import Field
from elixir import String
from elixir import using_options, has_many
from sqlalchemy.dialects.mysql import SMALLINT, INTEGER

from .base import Base


class NsService(Base):
    using_options(tablename='ns_service')

    id = Field(INTEGER(unsigned=True), colname='serviceID', primary_key=True)
    service_name = Field(
        String(length=64),
        colname='serviceName',
        required=True,
        unique=True
    )
    proto = Field(String(length=16), required=True)
    port = Field(SMALLINT(display_width=5, unsigned=True), required=True)

    has_many(
        'params',
        of_kind='NsServiceParam',
        inverse='service'
    )
