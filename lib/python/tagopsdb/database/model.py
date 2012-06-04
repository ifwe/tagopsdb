from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TINYINT, BOOLEAN
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import func

from meta import Base


ns_service_binds = Table(u'ns_service_binds', Base.metadata,
    Column(u'serviceID', INTEGER(unsigned=True), nullable=False),
    Column(u'monitorID', INTEGER(unsigned=True), nullable=False),
    ForeignKeyConstraint(['serviceID'], ['ns_service.serviceID'],
                         ondelete='cascade'),
    ForeignKeyConstraint(['monitorID'], ['ns_monitor.monitorID'],
                         ondelete='cascade'),
    mysql_engine='InnoDB', mysql_charset='utf8',
)


class AppDefinitions(Base):
    __tablename__ = 'app_definitions'

    AppID = Column(u'AppID', SMALLINT(display_width=2), primary_key=True,
                   nullable=False)
    Production_VlanID = Column(u'Production_VlanID', INTEGER(),
                               nullable=False)
    Development_VlanID = Column(u'Development_VlanID', INTEGER(),
                                nullable=False)
    Staging_VlanID = Column(u'Staging_VlanID', INTEGER(), nullable=False)
    distribution = Column(u'distribution', Enum(u'co54', u'rh53', u'co60',
                          u'co62'), default='co54', server_default='co54')
    appType = Column(u'appType', VARCHAR(length=100), nullable=False)
    warName = Column(u'warName', VARCHAR(length=100))
    jarName = Column(u'jarName', VARCHAR(length=100))
    contextPath = Column(u'contextPath', VARCHAR(length=100))
    hostBase = Column(u'hostBase', VARCHAR(length=100))
    svnRevision = Column(u'svnRevision', VARCHAR(length=100))
    hudsonRevision = Column(u'hudsonRevision', VARCHAR(length=100))
    puppetClass = Column(u'puppetClass', VARCHAR(length=100), nullable=False,
                         default='baseclass', server_default='baseclass')
    specID = Column(u'specID', INTEGER(), nullable=False)
    GangliaID = Column(u'GangliaID', INTEGER(), default=1, server_default='1')
    description = Column(u'description', VARCHAR(length=100))

    __table_args__ = (
        ForeignKeyConstraint(['Production_VlanID'], ['vlans.VlanID']),
        ForeignKeyConstraint(['Development_VlanID'], ['vlans.VlanID']),
        ForeignKeyConstraint(['Staging_VlanID'], ['vlans.VlanID']),
        ForeignKeyConstraint(['specID'], ['host_specs.specID']),
        ForeignKeyConstraint(['GangliaID'], ['ganglia.GangliaID']),
        { 'mysql_engine' : 'InnoDB', },
    )


class Asset(Base):
    __tablename__ = 'asset'

    AssetID = Column(u'AssetID', INTEGER(), primary_key=True, nullable=False)
    HostID = Column(u'HostID', INTEGER())
    NetworkID = Column(u'NetworkID', INTEGER())
    dateReceived = Column(u'dateReceived', DATE())
    description = Column(u'description', VARCHAR(length=20))
    oemSerial = Column(u'oemSerial', VARCHAR(length=30), unique=True)
    serviceTag = Column(u'serviceTag', VARCHAR(length=20))
    taggedSerial = Column(u'taggedSerial', VARCHAR(length=20))
    invoiceNumber = Column(u'invoiceNumber', VARCHAR(length=20))
    locationSite = Column(u'locationSite', VARCHAR(length=20))
    locationOwner = Column(u'locationOwner', VARCHAR(length=20))
    costPerItem = Column(u'costPerItem', VARCHAR(length=20))
    dateOfInvoice = Column(u'dateOfInvoice', DATE())
    warrantyStart = Column(u'warrantyStart', DATE())
    warrantyEnd = Column(u'warrantyEnd', DATE())
    warrantyLevel = Column(u'warrantyLevel', VARCHAR(length=20))
    warrantyID = Column(u'warrantyID', VARCHAR(length=20))
    vendorContact = Column(u'vendorContact', VARCHAR(length=20))

    __table_args__ = (
        ForeignKeyConstraint(['HostID'], ['hosts.HostID'],
                             ondelete='cascade'),
        ForeignKeyConstraint(['NetworkID'], ['networkDevice.NetworkID'],
                             ondelete='cascade'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class Cname(Base):
    __tablename__ = 'cname'

    CnameID = Column(u'CnameID', INTEGER(), primary_key=True, nullable=False)
    name = Column(u'name', VARCHAR(length=40), unique=True)
    IpID = Column(u'IpID', INTEGER())
    ZoneID = Column(u'ZoneID', INTEGER())

    __table_args__ = (
        ForeignKeyConstraint(['IpID'], ['host_ips.IpID'], onupdate='cascade',
                             ondelete='cascade'),
        ForeignKeyConstraint(['ZoneID'], ['zones.ZoneID'], onupdate='cascade',
                             ondelete='cascade'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class Deployments(Base):
    __tablename__ = 'deployments'

    DeploymentID = Column(u'DeploymentID', INTEGER(), primary_key=True,
                          nullable=False)
    declarer = Column(u'declarer', VARCHAR(length=255), nullable=False)
    declared = Column(u'declared', DATETIME(), nullable=False)
    PackageID = Column(u'PackageID', INTEGER(), nullable=False, index=True)
    AppID = Column(u'AppID', SMALLINT(display_width=2), nullable=False,
                   index=True)
    declaration = Column(u'declaration', Enum(u'deploy', u'validate',
                         u'invalidate'), nullable=False)
    environment = Column(u'environment', VARCHAR(length=15), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['PackageID'], ['packages.PackageID']),
        ForeignKeyConstraint(['AppID'], ['app_definitions.AppID']),
        UniqueConstraint('PackageID', 'AppID', 'declaration', 'environment',
                         name='unique_deployments'),
        { 'mysql_engine' : 'InnoDB', },
    )


class Environments(Base):
    __tablename__ = 'environments'

    environment = Column(u'environment', VARCHAR(length=15), primary_key=True,
                         nullable=False)
    domain = Column(u'domain', VARCHAR(length=32), nullable=False,
                    unique=True)

    __table_args__ = (
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class Ganglia(Base):
    __tablename__ = 'ganglia'

    GangliaID = Column(u'GangliaID', INTEGER(), primary_key=True,
                       nullable=False)
    cluster_name = Column(u'cluster_name', VARCHAR(length=50))
    production_ip = Column(u'production_ip', VARCHAR(length=15),
                           default='10.15.50.57',
                           server_default='10.15.50.57')
    production_ip2 = Column(u'production_ip2', VARCHAR(length=15),
                            default='10.15.50.54',
                            server_default='10.15.50.54')
    production_port = Column(u'production_port', INTEGER(display_width=5),
                             default=8649, server_default='8649')
    staging_ip = Column(u'staging_ip', VARCHAR(length=15),
                        default='10.99.20.54', server_default='10.99.20.54')
    staging_ip2 = Column(u'staging_ip2', VARCHAR(length=15),
                        default='10.99.20.30', server_default='10.99.20.30')
    staging_port = Column(u'staging_port', INTEGER(display_width=5),
                          default=8649, server_default='8649')
    development_ip = Column(u'development_ip', VARCHAR(length=15),
                            default='239.2.30.70',
                            server_default='239.2.30.70')
    development_ip = Column(u'development_ip2', VARCHAR(length=15),
                            default='239.2.30.70',
                            server_default='239.2.30.70')
    development_port = Column(u'development_port', INTEGER(display_width=5),
                              default=8649, server_default='8649')

    __table_args__ = (
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class Hosts(Base):
    __tablename__ = 'hosts'

    HostID = Column(u'HostID', INTEGER(), primary_key=True, nullable=False)
    SpecID = Column(u'SpecID', INTEGER())
    state = Column(u'state', Enum(u'baremetal', u'operational', u'repair',
                   u'parts', u'reserved'), nullable=False)
    hostname = Column(u'hostname', VARCHAR(length=30))
    arch = Column(u'arch', VARCHAR(length=10))
    kernelVersion = Column(u'kernelVersion', VARCHAR(length=20))
    distribution = Column(u'distribution', VARCHAR(length=20))
    timezone = Column(u'timezone', VARCHAR(length=10))
    AppID = Column(u'AppID', SMALLINT(display_width=2), nullable=False)
    cageLocation = Column(u'cageLocation', INTEGER())
    cabLocation = Column(u'cabLocation', VARCHAR(length=10))
    rackLocation = Column(u'rackLocation', INTEGER())
    consolePort = Column(u'consolePort', VARCHAR(length=11))
    powerPort = Column(u'powerPort', VARCHAR(length=10))
    powerCircuit = Column(u'powerCircuit', VARCHAR(length=10))
    environment = Column(u'environment', VARCHAR(length=15))

    __table_args__ = (
        ForeignKeyConstraint(['SpecID'], ['host_specs.specID']),
        ForeignKeyConstraint(['AppID'], ['app_definitions.AppID']),
        UniqueConstraint('cageLocation', 'cabLocation', 'consolePort'),
        UniqueConstraint('cageLocation', 'cabLocation', 'rackLocation'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )

class HostDeployments(Base):
    __tablename__ = 'host_deployments'

    HostDeploymentID = Column(u'HostDeploymentID', INTEGER(),
                              primary_key=True, nullable=False)
    realizer = Column(u'realizer', VARCHAR(length=255), nullable=False)
    realized = Column(u'realized', DATETIME(), nullable=False)
    DeploymentID = Column(u'DeploymentID', INTEGER(), nullable=False,
                          index=True)
    HostID = Column(u'HostID', INTEGER(), nullable=False, index=True)

    __table_args__ = (
        ForeignKeyConstraint(['DeploymentID'], ['deployments.DeploymentID']),
        ForeignKeyConstraint(['HostID'], ['hosts.HostID']),
        { 'mysql_engine' : 'InnoDB', },
    )


class HostInterfaces(Base):
    __tablename__ = 'host_interfaces'

    InterfaceID = Column(u'InterfaceID', INTEGER(), primary_key=True,
                         nullable=False)
    HostID = Column(u'HostID', INTEGER(), index=True)
    NetworkID = Column(u'NetworkID', INTEGER(), index=True)
    interfaceName = Column(u'interfaceName', VARCHAR(length=10))
    macAddress = Column(u'macAddress', VARCHAR(length=18), unique=True)
    PortID = Column(u'PortID', INTEGER(), unique=True, index=True)

    __table_args__ = (
        ForeignKeyConstraint(['HostID'], ['hosts.HostID'],
                             ondelete='cascade'),
        ForeignKeyConstraint(['NetworkID'], ['networkDevice.NetworkID'],
                             ondelete='cascade'),
        ForeignKeyConstraint(['PortID'], ['ports.PortID']),
        UniqueConstraint('HostID', 'interfaceName'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class HostIps(Base):
    __tablename__ = 'host_ips'

    IpID = Column(u'IpID', INTEGER(), primary_key=True, nullable=False)
    InterfaceID = Column(u'InterfaceID', INTEGER(), nullable=False,
                         index=True)
    SubnetID = Column(u'SubnetID', INTEGER(), nullable=False, unique=True,
                      index=True)
    virtualIP = Column(u'virtualIP', VARCHAR(length=20))
    nsVIP = Column(u'nsVIP', VARCHAR(length=30))
    ARecord = Column(u'ARecord', VARCHAR(length=200))
    comments = Column(u'comments', VARCHAR(length=200))

    __table_args__ = (
        ForeignKeyConstraint(['InterfaceID'], ['host_interfaces.InterfaceID'],
                             ondelete='cascade'),
        ForeignKeyConstraint(['SubnetID'], ['subnet.SubnetID'],
                             ondelete='cascade'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class HostSpecs(Base):
    __tablename__ = 'host_specs'

    specID = Column(u'specID', INTEGER(), primary_key=True, nullable=False)
    gen = Column(u'gen', VARCHAR(length=4))
    memorySize = Column(u'memorySize', VARCHAR(length=5), nullable=False)
    cores = Column(u'cores', SMALLINT(display_width=2), nullable=False)
    cpuSpeed = Column(u'cpuSpeed', VARCHAR(length=10), nullable=False)
    diskSize = Column(u'diskSize', VARCHAR(length=6), nullable=False)
    vendor = Column(u'vendor', VARCHAR(length=20))
    expansions = Column(u'expansions', TEXT())

    __table_args__ = (
        { 'mysql_engine' : 'InnoDB', },
    )


class HudsonLocations(Base):
    __tablename__ = 'hudsonLocations'

    hudLocID = Column(u'hudLocID', INTEGER(), primary_key=True,
                      nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False, unique=True)
    path = Column(u'path', VARCHAR(length=255), nullable=False, unique=True)
    pkg_name = Column(u'pkg_name', VARCHAR(length=255), nullable=False,
                      unique=True)

    __table_args__ = (
        { 'mysql_engine' : 'InnoDB', },
    )


class Iloms(Base):
    __tablename__ = 'iloms'

    ILomID = Column(u'ILomID', INTEGER(), primary_key=True, nullable=False)
    HostID = Column(u'HostID', INTEGER(), unique=True, index=True)
    SubnetID = Column(u'SubnetID', INTEGER(), nullable=False, unique=True,
                      index=True)
    macAddress = Column(u'macAddress', VARCHAR(length=18), unique=True)
    PortID = Column(u'PortID', INTEGER(), unique=True, index=True)
    ARecord = Column(u'ARecord', VARCHAR(length=200))
    comments = Column(u'comments', VARCHAR(length=200))

    __table_args__ = (
        ForeignKeyConstraint(['HostID'], ['hosts.HostID'],
                             ondelete='cascade'),
        ForeignKeyConstraint(['SubnetID'], ['subnet.SubnetID'],
                             ondelete='cascade'),
        ForeignKeyConstraint(['PortID'], ['ports.PortID'],
                             ondelete='cascade'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class Modules(Base):
    __tablename__ = 'modules'

    ModuleID = Column(u'ModuleID', INTEGER(), primary_key=True,
                      nullable=False)
    NetworkID = Column(u'NetworkID', INTEGER())
    modelNumber = Column(u'modelNumber', VARCHAR(length=20))

    __table_args__ = (
        ForeignKeyConstraint(['NetworkID'], ['networkDevice.NetworkID'],
                             ondelete='cascade'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class NetworkDevice(Base):
    __tablename__ = 'networkDevice'

    NetworkID = Column(u'NetworkID', INTEGER(), primary_key=True,
                       nullable=False)
    systemName = Column(u'systemName', VARCHAR(length=20), unique=True)
    model = Column(u'model', VARCHAR(length=50))
    hardwareCode = Column(u'hardwareCode', VARCHAR(length=20))
    softwareCode = Column(u'softwareCode', VARCHAR(length=20))

    __table_args__ = (
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class NsDevice(Base):
    __tablename__ = 'ns_device'

    deviceID = Column(u'deviceID', INTEGER(unsigned=True), primary_key=True,
                      nullable=False)
    proto = Column(u'proto', VARCHAR(length=6), nullable=False)
    host = Column(u'host', VARCHAR(length=32), nullable=False)

    __table_args__ = (
        UniqueConstraint('proto', 'host', name='proto_host'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class NsMonitor(Base):
    __tablename__ = 'ns_monitor'

    monitorID = Column(u'monitorID', INTEGER(unsigned=True), primary_key=True,
                       nullable=False)
    monitor = Column(u'monitor', VARCHAR(length=32), nullable=False,
                     unique=True)

    __table_args__ = (
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class NsService(Base):
    __tablename__ = 'ns_service'

    serviceID = Column(u'serviceID', INTEGER(unsigned=True), primary_key=True,
                       nullable=False)
    serviceName = Column(u'serviceName', VARCHAR(length=32), nullable=False,
                         unique=True)
    proto = Column(u'proto', VARCHAR(length=16), nullable=False)
    port = Column(u'port', SMALLINT(display_width=5, unsigned=True),
                  nullable=False)

    __table_args__ = (
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class NsServiceMax(Base):
    __tablename__ = 'ns_service_max'

    primaryID = Column(u'primaryID', INTEGER(), primary_key=True,
                       nullable=False)
    specID = Column(u'specID', INTEGER(), nullable=False)
    serviceID = Column(u'serviceID', INTEGER(unsigned=True), nullable=False)
    maxClient = Column(u'maxClient', INTEGER(unsigned=True), nullable=False,
                       default=0, server_default='0')
    maxReq = Column(u'maxReq', INTEGER(unsigned=True), nullable=False,
                    default=0, server_default='0')

    __table_args__ = (
        ForeignKeyConstraint(['specID'], ['host_specs.specID'],
                             ondelete='cascade'),
        ForeignKeyConstraint(['serviceID'], ['ns_service.serviceID'],
                             ondelete='cascade'),
        UniqueConstraint('specID', 'serviceID', name='specID_serviceID'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class NsServiceParams(Base):
    __tablename__ = 'ns_service_params'

    primaryID = Column(u'primaryID', INTEGER(), primary_key=True,
                       nullable=False)
    serviceID = Column(u'serviceID', INTEGER(unsigned=True), nullable=False)
    param = Column(u'param', VARCHAR(length=32), nullable=False)
    value = Column(u'value', VARCHAR(length=128), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['serviceID'], ['ns_service.serviceID'],
                             ondelete='cascade'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class NsVip(Base):
    __tablename__ = 'ns_vip'

    vipID = Column(u'vipID', INTEGER(unsigned=True), primary_key=True,
                   nullable=False)
    vserver = Column(u'vserver', VARCHAR(length=64), nullable=False)
    deviceID = Column(u'deviceID', INTEGER(unsigned=True), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['deviceID'], ['ns_device.deviceID'],
                             ondelete='cascade'),
        UniqueConstraint('deviceID', 'vserver', name='device_vserver'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class NsVipBinds(Base):
    __tablename__ = 'ns_vip_binds'

    primaryID = Column(u'primaryID', INTEGER(), primary_key=True,
                       nullable=False)
    appID = Column(u'appID', SMALLINT(display_width=6), nullable=False)
    environment = Column(u'environment', VARCHAR(length=15), nullable=False)
    vipID = Column(u'vipID', INTEGER(unsigned=True), nullable=False)
    serviceID = Column(u'serviceID', INTEGER(unsigned=True), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['appID'], ['app_definitions.AppID'],
                             ondelete='cascade'),
        ForeignKeyConstraint(['vipID'], ['ns_vip.vipID'], ondelete='cascade'),
        ForeignKeyConstraint(['serviceID'], ['ns_service.serviceID'],
                             ondelete='cascade'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class NsWeight(Base):
    __tablename__ = 'ns_weight'

    primaryID = Column(u'primaryID', INTEGER(), primary_key=True,
                       nullable=False)
    vipID = Column(u'vipID', INTEGER(unsigned=True), nullable=False)
    specID = Column(u'specID', INTEGER(), nullable=False)
    weight = Column(u'weight', TINYINT(display_width=3, unsigned=True),
                    nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['vipID'], ['ns_vip.vipID'], ondelete='cascade'),
        ForeignKeyConstraint(['specID'], ['host_specs.specID'],
                             ondelete='cascade'),
        UniqueConstraint('vipID', 'specID', name='vipID_specID'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class Packages(Base):
    __tablename__ = 'packages'

    PackageID = Column(u'PackageID', INTEGER(), primary_key=True,
                       nullable=False)
    pkg_name = Column(u'pkg_name', VARCHAR(length=255), nullable=False)
    version = Column(u'version', VARCHAR(length=63), nullable=False)
    revision = Column(u'revision', VARCHAR(length=63), nullable=False)
    created = Column(u'created', DATETIME(), nullable=False)
    creator = Column(u'creator', VARCHAR(length=255), nullable=False)
    builder = Column(u'builder', Enum(u'hudson', u'developer', u'tagconfig'),
                     nullable=False, default='developer',
                     server_default='developer')

    __table_args__ = (
        UniqueConstraint('pkg_name', 'version', 'revision', 'builder',
                         name='unique_package'),
        { 'mysql_engine' : 'InnoDB', },
    )


class PackageLocations(Base):
    __tablename__ = 'package_locations'

    pkgLocationID = Column(u'pkgLocationID', INTEGER(), primary_key=True,
                           nullable=False)
    pkg_type = Column(u'pkg_type', VARCHAR(length=255), nullable=False)
    pkg_name = Column(u'pkg_name', VARCHAR(length=255), nullable=False,
                      unique=True)
    app_name = Column(u'app_name', VARCHAR(length=255), nullable=False,
                      unique=True)
    path = Column(u'path', VARCHAR(length=255), nullable=False, unique=True)
    environment = Column(u'environment', BOOLEAN(), nullable=False)

    __table_args__ = (
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )

    def __init__(self, pkg_type, pkg_name, app_name, path, environment=False):
        """ """

        self.pkg_type = pkg_type
        self.pkg_name = pkg_name
        self.app_name = app_name
        self.path = path
        self.environment = environment


class Ports(Base):
    __tablename__ = 'ports'

    PortID = Column(u'PortID', INTEGER(), primary_key=True, nullable=False)
    NetworkID = Column(u'NetworkID', INTEGER())
    portNumber = Column(u'portNumber', VARCHAR(length=20))
    description = Column(u'description', VARCHAR(length=50))
    speed = Column(u'speed', VARCHAR(length=20))
    duplex = Column(u'duplex', VARCHAR(length=20))

    __table_args__ = (
        ForeignKeyConstraint(['NetworkID'], ['networkDevice.NetworkID'],
                             ondelete='cascade'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )

    def __init__(self, NetworkID=None, portNumber=None, description=None,
                 speed=None, duplex=None):
        """ """

        self.NetworkID = NetworkID
        self.portNumber = portNumber
        self.description = description
        self.speed = speed
        self.duplex = duplex


class ProcessorInfo(Base):
    __tablename__ = 'processor_info'

    processorId = Column(u'processorId', INTEGER(), primary_key=True,
                         nullable=False)
    cores = Column(u'cores', INTEGER())
    capacity = Column(u'capacity', FLOAT())
    hyperthreaded = Column(u'hyperthreaded', INTEGER())
    processor_name = Column(u'processor_name', VARCHAR(length=20))
    clock_speed = Column(u'clock_speed', FLOAT())


class ServiceEvent(Base):
    __tablename__ = 'serviceEvent'

    ServiceID = Column(u'ServiceID', INTEGER(), primary_key=True,
                       nullable=False)
    HostID = Column(u'HostID', INTEGER())
    NetworkID = Column(u'NetworkID', INTEGER())
    serviceStatus = Column(u'serviceStatus', VARCHAR(length=100))
    powerStatus = Column(u'powerStatus', VARCHAR(length=10))
    vendorTicket = Column(u'vendorTicket', VARCHAR(length=20))
    comments = Column(u'comments', TEXT())
    serviceDate = Column(u'serviceDate', TIMESTAMP(), nullable=False,
                         default=func.current_timestamp(),
                         onupdate=func.current_timestamp(),
                         server_onupdate=func.current_timestamp())

    __table_args__ = (
        ForeignKeyConstraint(['HostID'], ['hosts.HostID'],
                             ondelete='cascade'),
        ForeignKeyConstraint(['NetworkID'], ['networkDevice.NetworkID'],
                             ondelete='cascade'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class SpecProcessor(Base):
    __tablename__ = 'spec_processor'

    specId = Column(u'specId', INTEGER(), primary_key=True, nullable=False)
    processorId = Column(u'processorId', INTEGER())


class SpecidToMaxclients(Base):
    __tablename__ = 'specid_to_maxclients'

    specID = Column(u'specID', INTEGER(), nullable=False)
    AppID = Column(u'AppID', SMALLINT(display_width=2), nullable=False)
    vip_maxclients = Column(u'vip_maxclients', VARCHAR(length=4),
                            nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('specID', 'AppID'),
        ForeignKeyConstraint(['specID'], ['host_specs.specID']),
        ForeignKeyConstraint(['AppID'], ['app_definitions.AppID']),
        { 'mysql_engine' : 'InnoDB', },
    )


class Subnet(Base):
    __tablename__ = 'subnet'

    SubnetID = Column(u'SubnetID', INTEGER(), primary_key=True,
                      nullable=False)
    VlanID = Column(u'VlanID', INTEGER())
    ipAddress = Column(u'ipAddress', VARCHAR(length=15), unique=True)
    netmask = Column(u'netmask', VARCHAR(length=15))
    gateway = Column(u'gateway', VARCHAR(length=15))
    ZoneID = Column(u'ZoneID', INTEGER())

    __table_args__ = (
        ForeignKeyConstraint(['VlanID'], ['vlans.VlanID'],
                             ondelete='cascade'),
        ForeignKeyConstraint(['ZoneID'], ['zones.ZoneID']),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class UsageStats(Base):
    __tablename__ = 'usage_stats'

    primaryID = Column(u'primaryID', INTEGER(), primary_key=True,
                       nullable=False)
    date = Column(u'date', DATE())
    appType = Column(u'appType', VARCHAR(length=100))
    servers = Column(u'servers', INTEGER(display_width=5))
    cores = Column(u'cores', INTEGER(display_width=6))
    cpu = Column(u'cpu', INTEGER(display_width=6))
    environment = Column(u'environment', Enum(u'production', u'staging',
                         u'development'))


class UsageStats2(Base):
    __tablename__ = 'usage_stats_2'

    hostname = Column(u'hostname', VARCHAR(length=30), primary_key=True,
                      nullable=False, default='', server_default='')
    util = Column(u'util', FLOAT())


class Vlans(Base):
    __tablename__ = 'vlans'

    VlanID = Column(u'VlanID', INTEGER(), primary_key=True, nullable=False)
    name = Column(u'name', VARCHAR(length=20))
    description = Column(u'description', VARCHAR(length=50))

    __table_args__ = (
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class Zones(Base):
    __tablename__ = 'zones'

    ZoneID = Column(u'ZoneID', INTEGER(), primary_key=True, nullable=False)
    zoneName = Column(u'zoneName', VARCHAR(length=30))
    mxPriority = Column(u'mxPriority', INTEGER())
    mxHostID = Column(u'mxHostID', VARCHAR(length=30))
    nsPriority = Column(u'nsPriority', INTEGER())
    nameserver = Column(u'nameserver', VARCHAR(length=30))

    __table_args__ = (
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
