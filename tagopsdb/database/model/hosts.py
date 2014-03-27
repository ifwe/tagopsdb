from sqlalchemy import Column, Enum, UniqueConstraint, ForeignKey, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from sqlalchemy.orm import relationship

from .base import Base


class Hosts(Base):
    __tablename__ = 'hosts'

    id = Column(u'HostID', INTEGER(), primary_key=True)
    spec_id = Column(u'SpecID', INTEGER(), ForeignKey('host_specs.specID'))
    state = Column(Enum(u'baremetal', u'operational', u'repair', u'parts',
                   u'reserved', u'escrow'), nullable=False)
    hostname = Column(VARCHAR(length=30))
    arch = Column(VARCHAR(length=10))
    kernel_version = Column(u'kernelVersion', VARCHAR(length=20))
    distribution = Column(VARCHAR(length=20))
    timezone = Column(VARCHAR(length=10))
    app_id = Column(u'AppID', SMALLINT(display_width=6),
                    ForeignKey('app_definitions.AppID'), nullable=False)
    cage_location = Column(u'cageLocation', INTEGER())
    cab_location = Column(u'cabLocation', VARCHAR(length=10))
    section = Column(VARCHAR(length=10))
    rack_location = Column(u'rackLocation', INTEGER())
    console_port = Column(u'consolePort', VARCHAR(length=11))
    power_port = Column(u'powerPort', VARCHAR(length=10))
    power_circuit = Column(u'powerCircuit', VARCHAR(length=10))
    environment = Column(VARCHAR(length=15))

    host_deployments = relationship('HostDeployments')
    host_interfaces = relationship('HostInterfaces', backref='host')
    host_spec = relationship('HostSpecs', uselist=False, backref='hosts')
    ilom = relationship('Iloms', uselist=False, backref='host')
    service_events = relationship('ServiceEvent', backref='host')

    __table_args__ = (
        UniqueConstraint(u'cageLocation', u'cabLocation', u'consolePort'),
        UniqueConstraint(u'cageLocation', u'cabLocation', u'rackLocation'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'},
    )

    def __init__(self, spec_id, state, hostname, arch, kernel_version,
                 distribution, timezone, app_id, cage_location, cab_location,
                 section, rack_location, console_port, power_port,
                 power_circuit, environment):
        """ """

        self.spec_id = spec_id
        self.state = state
        self.hostname = hostname
        self.arch = arch
        self.kernel_version = kernel_version
        self.distribution = distribution
        self.timezone = timezone
        self.app_id = app_id
        self.cage_location = cage_location
        self.cab_location = cab_location
        self.section = section
        self.rack_location = rack_location
        self.console_port = console_port
        self.power_port = power_port
        self.power_circuit = power_circuit
        self.environment = environment
