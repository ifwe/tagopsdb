from elixir import Field
from elixir import Integer, String
from elixir import using_options
from sqlalchemy.dialects.mysql import SMALLINT

from .base import Base


class NsService(Base):
    using_options(tablename='ns_service')

    id = Field(Integer, colname='serviceID', primary_key=True)
    service_name = Field(
        String(length=64),
        colname='serviceName',
        nullable=False,
        unique=True
    )
    proto = Field(String(length=16), nullable=False)
    port = Field(SMALLINT(display_width=5, unsigned=True), nullable=False)
