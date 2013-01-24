from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TINYINT, BOOLEAN
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import func

from meta import Base


jmx_attributes = Table(u'jmx_attributes', Base.metadata,
    Column(u'groupName', VARCHAR(length=25)),
    Column(u'obj', VARCHAR(length=300)),
    Column(u'attr', VARCHAR(length=300)),
    Column(u'appID', SMALLINT(display_width=2)),
    Column(u'GangliaID', INTEGER()),
    ForeignKeyConstraint(['appID'], ['app_definitions.AppID']),
    ForeignKeyConstraint(['GangliaID'], ['ganglia.GangliaID']),
    mysql_engine='InnoDB', mysql_charset='latin1',
    )


ns_service_binds = Table(u'ns_service_binds', Base.metadata,
    Column(u'serviceID', INTEGER(unsigned=True), nullable=False),
    Column(u'monitorID', INTEGER(unsigned=True), nullable=False),
    ForeignKeyConstraint(['serviceID'], ['ns_service.serviceID'],
                         ondelete='cascade'),
    ForeignKeyConstraint(['monitorID'], ['ns_monitor.monitorID'],
                         ondelete='cascade'),
    UniqueConstraint('serviceID', 'monitorID', name='serviceID_monitorID'),
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
    hostBase = Column(u'hostBase', VARCHAR(length=100))
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


    def __init__(self, Production_VlanID, Development_VlanID, Staging_VlanID,
                 distribution, appType, hostBase, puppetClass, specID,
                 GangliaID, description):
        """ """

        self.Production_VlanID = Production_VlanID
        self.Development_VlanID = Development_VlanID
        self.Staging_VlanID = Staging_VlanID
        self.distribution = distribution
        self.appType = appType
        self.hostBase = hostBase
        self.puppetClass = puppetClass
        self.specID = specID
        self.GangliaID = GangliaID
        self.description = description


    def __repr__(self):
        """ """

        return '<AppDefinitions("%s", "%s", "%s", "%s", "%s", "%s", "%s", ' \
               '"%s", "%s", "%s")>' \
               % (self.Production_VlanID, self.Development_VlanID,
                  self.Staging_VlanID, self.distribution, self.appType,
                  self.hostBase, self.puppetClass, self.specID,
                  self.GangliaID, self.description)


class AppDeployments(Base):
    __tablename__ = 'app_deployments'

    AppDeploymentID = Column('AppDeploymentID', INTEGER(), primary_key=True,
                             nullable=False)
    DeploymentID = Column('DeploymentID', INTEGER(), nullable=False)
    AppID = Column('AppID', SMALLINT(display_width=2), nullable=False)
    user = Column('user', VARCHAR(length=32), nullable=False)
    status = Column('status', Enum('complete', 'incomplete', 'inprogress',
                    'invalidated', 'validated'), nullable=False)
    environment = Column('environment', VARCHAR(length=15), nullable=False)
    realized = Column('realized', TIMESTAMP(), nullable=False,
                      default=func.current_timestamp(),
                      server_default=func.current_timestamp())

    __table_args__ = (
        ForeignKeyConstraint(['DeploymentID'], ['deployments.DeploymentID'],
                             ondelete='cascade'),
        ForeignKeyConstraint(['AppID'], ['app_definitions.AppID'],
                             ondelete='cascade'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


    def __init__(self, DeploymentID, AppID, user, status, environment,
                 realized):
        """ """

        self.DeploymentID = DeploymentID
        self.AppID = AppID
        self.user = user
        self.status = status
        self.environment = environment
        self.realized = realized


    def __repr__(self):
        """ """

        return '<AppDeployments("%s", "%s", "%s", "%s", "%s", "%s")>' \
               % (self.DeploymentID, self.AppID, self.user, self.status,
                  self.environment, self.realized)


class AppHipchatRooms(Base):
    __tablename__ = 'app_hipchat_rooms'

    AppID = Column(u'AppID', SMALLINT(display_width=2), nullable=False)
    roomID = Column(u'roomID', INTEGER(), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('AppID', 'roomID'),
        ForeignKeyConstraint(['AppID'], ['app_definitions.AppID'],
                             ondelete='cascade'),
        ForeignKeyConstraint(['roomID'], ['hipchat.roomID'],
                             ondelete='cascade'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


    def __init__(self, AppID, roomID):
        """ """

        self.AppID = AppID
        self.roomID = roomID


    def __repr__(self):
        """ """

        return '<AppHipchatRooms("%s", "%s")>' % (self.AppID, self.roomID)


class AppPackages(Base):
    __tablename__ = 'app_packages'

    pkgLocationID = Column('pkgLocationID', INTEGER(), nullable=False)
    AppID = Column('AppID', SMALLINT(display_width=2), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('pkgLocationID', 'AppID'),
        ForeignKeyConstraint(['pkgLocationID'],
                             ['package_locations.pkgLocationID'],
                             ondelete='cascade'),
        ForeignKeyConstraint(['AppID'], ['app_definitions.AppID'],
                             ondelete='cascade'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


    def __init__(self, pkgLocationID, AppID):
        """ """

        self.pkgLocationID = pkgLocationID
        self.AppID = AppID


    def __repr__(self):
        """ """

        return '<AppPackages("%s", "%s")>' % (self.pkgLocationID, self.AppID)


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
    name = Column(u'name', VARCHAR(length=40))
    IpID = Column(u'IpID', INTEGER())
    ZoneID = Column(u'ZoneID', INTEGER())

    __table_args__ = (
        ForeignKeyConstraint(['IpID'], ['host_ips.IpID'], onupdate='cascade',
                             ondelete='cascade'),
        ForeignKeyConstraint(['ZoneID'], ['zones.ZoneID'], onupdate='cascade',
                             ondelete='cascade'),
        UniqueConstraint('name', 'ZoneID', name='name_ZoneID'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class Deployments(Base):
    __tablename__ = 'deployments'

    DeploymentID = Column(u'DeploymentID', INTEGER(), primary_key=True,
                          nullable=False)
    PackageID = Column(u'PackageID', INTEGER(), nullable=False)
    user = Column(u'user', VARCHAR(length=32), nullable=False)
    dep_type = Column(u'dep_type', Enum('deploy', 'rollback'), nullable=False)
    declared = Column(u'declared', TIMESTAMP(), nullable=False,
                      default=func.current_timestamp(),
                      server_default=func.current_timestamp())

    __table_args__ = (
        ForeignKeyConstraint(['PackageID'], ['packages.PackageID'],
                             ondelete='cascade'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


    def __init__(self, PackageID, user, dep_type, declared):
        """ """

        self.PackageID = PackageID
        self.user = user
        self.dep_type = dep_type
        self.declared = declared


    def __repr__(self):
        """ """

        return '<Deployments("%s", "%s", "%s", "%s")>' \
               % (self.PackageID, self.user, self.dep_type, self.declared)


class Environments(Base):
    __tablename__ = 'environments'

    environment = Column(u'environment', VARCHAR(length=15), primary_key=True,
                         nullable=False)
    domain = Column(u'domain', VARCHAR(length=32), nullable=False,
                    unique=True)
    domain = Column(u'prefix', VARCHAR(length=1), nullable=False)

    __table_args__ = (
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class Ganglia(Base):
    __tablename__ = 'ganglia'

    GangliaID = Column(u'GangliaID', INTEGER(), primary_key=True,
                       nullable=False)
    cluster_name = Column(u'cluster_name', VARCHAR(length=50))
    port = Column(u'port', INTEGER(display_width=5), nullable=False,
                  default='8649', server_default='8649')

    __table_args__ = (
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


class Hipchat(Base):
    __tablename__ = 'hipchat'

    roomID = Column(u'roomID', INTEGER(), primary_key=True, nullable=False)
    room_name = Column(u'room_name', VARCHAR(length=50), unique=True)

    __table_args__ = (
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


    def __init__(self, room_name):
        """ """

        self.room_name = room_name


    def __repr__(self):
        """ """

        return '<Hipchat("%s", "%s")>' % (self.roomID, self.room_name)


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


    def __init__(self, SpecID, state, hostname, arch, kernelVersion,
                 distribution, timezone, AppID, cageLocation, cabLocation,
                 rackLocation, consolePort, powerPort, powerCircuit,
                 environment):
        """ """

        self.SpecID = SpecID
        self.state = state
        self.hostname = hostname
        self.arch = arch
        self.kernelVersion = kernelVersion
        self.distribution = distribution
        self.timezone = timezone
        self.AppID = AppID
        self.cageLocation = cageLocation
        self.cabLocation = cabLocation
        self.rackLocation = rackLocation
        self.consolePort = consolePort
        self.powerPort = powerPort
        self.powerCircuit = powerCircuit
        self.environment = environment


    def __repr__(self):
        """ """

        return '<Hosts(%r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, ' \
               '%r, %r, %r)>' \
               % (self.SpecID, self.state, self.hostname, self.arch,
                  self.kernelVersion, self.distribution, self.timezone,
                  self.AppID, self.cageLocation, self.cabLocation,
                  self.rackLocation, self.consolePort, self.powerPort,
                  self.powerCircuit, self.environment)


class HostDeployments(Base):
    __tablename__ = 'host_deployments'

    HostDeploymentID = Column('HostDeploymentID', INTEGER(), primary_key=True,
                              nullable=False)
    DeploymentID = Column('DeploymentID', INTEGER(), nullable=False)
    HostID = Column('HostID', INTEGER(), nullable=False)
    user = Column('user', VARCHAR(length=32), nullable=False)
    status = Column('status', Enum('inprogress', 'ok', 'failed'),
                    nullable=False)
    realized = Column('realized', TIMESTAMP(), nullable=False,
                      default=func.current_timestamp(),
                      server_default=func.current_timestamp())

    __table_args__ = (
        ForeignKeyConstraint(['DeploymentID'], ['deployments.DeploymentID'],
                             ondelete='cascade'),
        ForeignKeyConstraint(['HostID'], ['hosts.HostID'],
                             ondelete='cascade'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


    def __init__(self, DeploymentID, HostID, user, status, realized):
        """ """

        self.DeploymentID = DeploymentID
        self.HostID = HostID
        self.user = user
        self.status = status
        self.realized = realized


    def __repr__(self):
        """ """

        return '<HostDeployments("%s", "%s", "%s", "%s", "%s")>' \
               % (self.DeploymentID, self.HostID, self.user, self.status,
                  self.realized)


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
    priority = Column(u'priority', INTEGER(unsigned=True), nullable=False,
                      default=1, server_default='1')
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
    memorySize = Column(u'memorySize', INTEGER(display_width=4),
                        nullable=False)
    cores = Column(u'cores', SMALLINT(display_width=2), nullable=False)
    cpuSpeed = Column(u'cpuSpeed', INTEGER(display_width=6), nullable=False)
    diskSize = Column(u'diskSize', INTEGER(display_width=6), nullable=False)
    vendor = Column(u'vendor', VARCHAR(length=20))
    model = Column(u'model', VARCHAR(length=20))
    control = Column(u'control', Enum(u'digi', u'ipmi', u'vmcontrol'))
    expansions = Column(u'expansions', TEXT())

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
        UniqueConstraint('appID', 'environment', 'vipID', 'serviceID',
                         name='nsVipBindsID'),
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
    created = Column(u'created', TIMESTAMP(), nullable=False,
                     default=func.current_timestamp(),
                     server_default=func.current_timestamp())
    creator = Column(u'creator', VARCHAR(length=255), nullable=False)
    builder = Column(u'builder', Enum(u'developer', u'hudson', u'jenkins'),
                     nullable=False, default='developer',
                     server_default='developer')
    project_type = Column(u'project_type', Enum(u'application', u'tagconfig'),
                          nullable=False, default='application',
                          server_default='application')

    __table_args__ = (
        UniqueConstraint('pkg_name', 'version', 'revision', 'builder',
                         name='unique_package'),
        { 'mysql_engine' : 'InnoDB', },
    )


    def __init__(self, pkg_name, version, revision, created, creator,
                 builder, project_type):
        """ """

        self.pkg_name = pkg_name
        self.version = version
        self.revision = revision
        self.created = created
        self.creator = creator
        self.builder = builder
        self.project_type = project_type


    def __repr__(self):
        """ """

        return '<Packages("%s", "%s", "%s", "%s", "%s", "%s", "%s")>' \
               % (self.pkg_name, self.version, self.revision, self.created,
                  self.creator, self.builder, self.project_type)


class PackageLocations(Base):
    __tablename__ = 'package_locations'

    pkgLocationID = Column(u'pkgLocationID', INTEGER(), primary_key=True,
                           nullable=False)
    project_type = Column(u'project_type', Enum(u'application', u'tagconfig'),
                          nullable=False, default='application',
                          server_default='application')
    pkg_type = Column(u'pkg_type', VARCHAR(length=255), nullable=False)
    pkg_name = Column(u'pkg_name', VARCHAR(length=255), nullable=False,
                      unique=True)
    app_name = Column(u'app_name', VARCHAR(length=255), nullable=False,
                      unique=True)
    path = Column(u'path', VARCHAR(length=255), nullable=False, unique=True)
    arch = Column(u'arch', Enum(u'i386', u'x86_64', u'noarch'),
                  nullable=False, default='noarch', server_default='noarch')
    build_host = Column(u'build_host', VARCHAR(length=30), nullable=False)
    environment = Column(u'environment', BOOLEAN(), nullable=False)

    __table_args__ = (
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


    def __init__(self, project_type, pkg_type, pkg_name, app_name, path, arch,
                 build_host, environment=False):
        """ """

        self.project_type = project_type
        self.pkg_type = pkg_type
        self.pkg_name = pkg_name
        self.app_name = app_name
        self.path = path
        self.arch = arch
        self.build_host = build_host
        self.environment = environment


    def __repr__(self):
        """ """

        return '<PackageLocations("%s", "%s", "%s", "%s", "%s", "%s", ' \
               '"%s", "%s")>' % (self.project_type, self.pkg_type,
                                 self.pkg_name, self.app_name, self.path,
                                 self.arch, self.build_host, self.environment)


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
    user = Column(u'user', VARCHAR(length=20))
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
