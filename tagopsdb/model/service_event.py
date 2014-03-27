from elixir import Field
from elixir import String, Integer, Text, DateTime
from elixir import using_options, belongs_to
from sqlalchemy.sql.expression import func

from .base import Base


class ServiceEvent(Base):
    using_options(tablename='serviceEvent')

    id = Field(Integer, colname='ServiceID', primary_key=True)
    user = Field(String(length=20))
    service_status = Field(String(length=100), colname='serviceStatus')
    power_status = Field(String(length=100), colname='powerStatus')
    vendor_ticket = Field(String(length=20), colname='vendorTicket')
    comments = Field(Text)
    service_date = Field(
        DateTime,
        colname='serviceDate',
        required=True,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        server_onupdate=func.current_timestamp()
    )

    belongs_to('host', of_kind='Host', colname='HostID', ondelete='cascade')
