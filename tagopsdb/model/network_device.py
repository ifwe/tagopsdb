from elixir import Field
from elixir import String, Integer
from elixir import using_options, has_many

from .base import Base


class NetworkDevice(Base):
    using_options(tablename='networkDevice')

    id = Field(Integer, colname='NetworkID', primary_key=True)
    system_name = Field(String(length=20), colname='systemName', unique=True)
    model = Field(String(length=50))
    hardware_code = Field(String(length=20), colname='hardwareCode')
    software_code = Field(String(length=20), colname='softwareCode')

    has_many(
        'host_interfaces',
        of_kind='HostInterface',
        inverse='network',
    )

    has_many(
        'ports',
        of_kind='Port',
        inverse='network',
    )
