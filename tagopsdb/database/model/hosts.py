from elixir import Field
from elixir import String, Integer, Enum
from elixir import using_options, using_table_options, belongs_to
from sqlalchemy import UniqueConstraint

from .base import Base


class Hosts(Base):
    using_options(tablename='hosts')
    using_table_options(
        UniqueConstraint('cageLocation', 'cabLocation', 'consolePort'),
        UniqueConstraint('cageLocation', 'cabLocation', 'rackLocation'),
    )

    id = Field(Integer, colname='HostID', primary_key=True)
    state = Field(
        Enum(
            'baremetal',
            'operational',
            'repair',
            'parts',
            'reserved',
            'escrow'
        ),
        required=True,
    )
    hostname = Field(String(length=30))
    arch = Field(String(length=10))
    kernel_version = Field(String(length=20), colname='kernelVersion')
    distribution = Field(String(length=20))
    timezone = Field(String(length=10))
    cage_location = Field(Integer, colname='cageLocation')
    cab_location = Field(String(length=10), colname='cabLocation')
    section = Field(String(length=10))
    rack_location = Field(Integer, colname='rackLocation')
    console_port = Field(String(length=11), colname='consolePort')
    power_port = Field(String(length=10), colname='powerPort')
    power_circuit = Field(String(length=10), colname='powerCircuit')
    environment = Field(String(length=15))

    belongs_to(
        'app',
        of_kind='AppDefinitions',
        colname='AppID',
        required=True
    )
    belongs_to('spec', of_kind='HostSpecs', colname='SpecID')
