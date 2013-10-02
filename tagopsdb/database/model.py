from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TINYINT, BOOLEAN, \
                                      MEDIUMTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func

from meta import Base


#
# Class and table definitions for schema
#


class Environments(Base):
    __tablename__ = 'environments'

    id = Column(u'environmentID', INTEGER(), primary_key=True)
    environment = Column(VARCHAR(length=15), nullable=False, unique=True)
    env = Column(VARCHAR(length=12), nullable=False, unique=True)
    domain = Column(VARCHAR(length=32), nullable=False, unique=True)
    prefix = Column(VARCHAR(length=1), nullable=False)


    def __init__(self, environment, env, domain, prefix):
        """ """

        self.environment = environment
        self.env = env
        self.domain = domain
        self.prefix = prefix


class Ganglia(Base):
    __tablename__ = 'ganglia'

    id = Column(u'GangliaID', INTEGER(), primary_key=True)
    cluster_name = Column(VARCHAR(length=50))
    port = Column(INTEGER(display_width=5), nullable=False, default='8649',
                  server_default='8649')


    def __init__(self, cluster_name, port):
        """ """

        self.cluster_name = cluster_name
        self.port = port


class Hipchat(Base):
    __tablename__ = 'hipchat'

    id = Column(u'roomID', INTEGER(), primary_key=True)
    room_name = Column(VARCHAR(length=50), nullable=False, unique=True)


    def __init__(self, room_name):
        """ """

        self.room_name = room_name


class HostSpecs(Base):
    __tablename__ = 'host_specs'

    id = Column(u'specID', INTEGER(), primary_key=True)
    gen = Column(VARCHAR(length=4))
    memory_size = Column(u'memorySize', INTEGER(display_width=4))
    cores = Column(SMALLINT(display_width=2), nullable=False)
    cpu_speed = Column(u'cpuSpeed', INTEGER(display_width=6))
    disk_size = Column(u'diskSize', INTEGER(display_width=6))
    vendor = Column(VARCHAR(length=20))
    model = Column(VARCHAR(length=20))
    control = Column(Enum(u'digi', u'ipmi', u'libvirt', u'vmware'))
    virtual = Column(BOOLEAN(), nullable=False, default=0, server_default='0')
    expansions = Column(MEDIUMTEXT())


    def __init__(self, gen, memory_size, cores, cpu_speed, disk_size, vendor,
                 model, control, virtual, expansions):
        """ """

        self.gen = gen
        self.memory_size = memory_size
        self.cores = cores
        self.cpu_speed = cpu_speed
        self.disk_size = disk_size
        self.vendor = vendor
        self.model = model
        self.control = control
        self.virtual = virtual
        self.expansions = expansions


class JmxAttributes(Base):
    __tablename__ = 'jmx_attributes'

    id = Column(u'jmx_attribute_id', INTEGER(), primary_key=True)
    obj = Column(VARCHAR(length=300), nullable=False)
    attr = Column(VARCHAR(length=300), nullable=False)
    g_group_name = Column(u'GgroupName', VARCHAR(length=25))


locks = Table(u'locks', Base.metadata,
    Column(u'val', VARCHAR(length=64), nullable=False, unique=True),
    Column(u'host', VARCHAR(length=32), nullable=False),
    mysql_engine='InnoDB', mysql_charset='utf8',
)


class NagCheckCommands(Base):
    __tablename__ = 'nag_check_commands'

    id = Column(INTEGER(), primary_key=True)
    command_name = Column(VARCHAR(length=32), nullable=False, unique=True)
    command_line = Column(VARCHAR(length=255), nullable=False)


class NagContactGroups(Base):
    __tablename__ = 'nag_contact_groups'

    id = Column(INTEGER(), primary_key=True)
    name = Column(VARCHAR(length=32), nullable=False, unique=True)
    alias = Column(VARCHAR(length=80))


class NagContacts(Base):
    __tablename__ = 'nag_contacts'

    id = Column(INTEGER(), primary_key=True)
    name = Column(VARCHAR(length=32), nullable=False, unique=True)
    alias = Column(VARCHAR(length=80))
    email = Column(VARCHAR(length=80))
    pager = Column(VARCHAR(length=80))


class NagTimePeriods(Base):
    __tablename__ = 'nag_time_periods'

    id = Column(INTEGER(), primary_key=True)
    name = Column(VARCHAR(length=32), nullable=False, unique=True)
    alias = Column(VARCHAR(length=80))
    sunday = Column(VARCHAR(length=32))
    monday = Column(VARCHAR(length=32))
    tuesday = Column(VARCHAR(length=32))
    wednesday = Column(VARCHAR(length=32))
    thursday = Column(VARCHAR(length=32))
    friday = Column(VARCHAR(length=32))
    saturday = Column(VARCHAR(length=32))


class NetworkDevice(Base):
    __tablename__ = 'networkDevice'

    id = Column(u'NetworkID', INTEGER(), primary_key=True)
    system_name = Column(u'systemName', VARCHAR(length=20), unique=True)
    model = Column(VARCHAR(length=50))
    hardware_code = Column(u'hardwareCode', VARCHAR(length=20))
    software_code = Column(u'softwareCode', VARCHAR(length=20))


    def __init__(self, system_name, model, hardware_code, software_code):
        """ """

        self.system_name = system_name
        self.model = model
        self.hardware_code = hardware_code
        self.software_code = software_code


class NsDevice(Base):
    __tablename__ = 'ns_device'

    id = Column(u'deviceID', INTEGER(unsigned=True), primary_key=True)
    proto = Column(VARCHAR(length=6), nullable=False)
    host = Column(VARCHAR(length=32), nullable=False)

    __table_args__ = (
        UniqueConstraint(u'proto', u'host', name=u'proto_host'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


    def __init__(self, proto, host):
        """ """

        self.proto = proto
        self.host = host


class NsMonitor(Base):
    __tablename__ = 'ns_monitor'

    id = Column(u'monitorID', INTEGER(unsigned=True), primary_key=True)
    monitor = Column(VARCHAR(length=32), nullable=False, unique=True)


    def __init__(self, monitor):
        """ """

        self.monitor = monitor


class NsService(Base):
    __tablename__ = 'ns_service'

    id = Column(u'serviceID', INTEGER(unsigned=True), primary_key=True)
    service_name = Column(u'serviceName', VARCHAR(length=64), nullable=False,
                          unique=True)
    proto = Column(VARCHAR(length=16), nullable=False)
    port = Column(SMALLINT(display_width=5, unsigned=True), nullable=False)


    def __init__(self, service_name, proto, port):
        """ """

        self.service_name = service_name
        self.proto = proto
        self.port = port


class PackageDefinitions(Base):
    __tablename__ = 'package_definitions'

    id = Column(u'pkg_def_id', INTEGER(), primary_key=True)
    deploy_type = Column(VARCHAR(length=30), nullable=False)
    validation_type = Column(VARCHAR(length=15), nullable=False)
    pkg_name = Column(VARCHAR(length=255), nullable=False)
    path = Column(VARCHAR(length=255), nullable=False)
    arch = Column(Enum('i386', 'x86_64', 'noarch'), nullable=False,
                  default='noarch', server_default='noarch')
    build_type = Column(Enum(u'developer', u'hudson', u'jenkins'),
                        nullable=False, default='jenkins',
                        server_default='jenkins')
    build_host = Column(VARCHAR(length=255), nullable=False)
    env_specific = Column(BOOLEAN(), nullable=False, default=0,
                          server_default='0')
    created = Column(TIMESTAMP(), nullable=False,
                     default=func.current_timestamp(),
                     server_default=func.current_timestamp())


    def __init__(self, deploy_type, validation_type, pkg_name, path, arch,
                 build_type, build_host, env_specific, created):
        """ """

        self.deploy_type = deploy_type
        self.validation_type = validation_type
        self.pkg_name = pkg_name
        self.path = path
        self.arch = arch
        self.build_type = build_type
        self.build_host = build_host
        self.env_specific = env_specific
        self.created = created


class PackageLocations(Base):
    __tablename__ = 'package_locations'

    id = Column(u'pkgLocationID', INTEGER(), primary_key=True)
    project_type = Column(Enum(u'application', u'kafka-config', u'tagconfig'),
                          nullable=False, default='application',
                          server_default='application')
    pkg_type = Column(VARCHAR(length=255), nullable=False)
    pkg_name = Column(VARCHAR(length=255), nullable=False, unique=True)
    app_name = Column(VARCHAR(length=255), nullable=False, unique=True)
    path = Column(VARCHAR(length=255), nullable=False, unique=True)
    arch = Column(Enum(u'i386', u'x86_64', u'noarch'), nullable=False,
                  default='noarch', server_default='noarch')
    build_host = Column(VARCHAR(length=30), nullable=False)
    environment = Column(BOOLEAN(), nullable=False)


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


class Packages(Base):
    __tablename__ = 'packages'

    id = Column(u'package_id', INTEGER(), primary_key=True)
    pkg_def_id = Column(INTEGER(),
                        ForeignKey(PackageDefinitions.id, ondelete='cascade'),
                        nullable=False)
    pkg_name = Column(VARCHAR(length=255), nullable=False)
    version = Column(VARCHAR(length=63), nullable=False)
    revision = Column(VARCHAR(length=63), nullable=False)
    created = Column(TIMESTAMP(), nullable=False,
                     default=func.current_timestamp(),
                     server_default=func.current_timestamp())
    creator = Column(VARCHAR(length=255), nullable=False)
    builder = Column(Enum(u'developer', u'hudson', u'jenkins'),
                     nullable=False, default='developer',
                     server_default='developer')
    project_type = Column(Enum(u'application', u'kafka-config', u'tagconfig'),
                          nullable=False, default='application',
                          server_default='application')

    __table_args__ = (
        UniqueConstraint(u'pkg_name', u'version', u'revision', u'builder',
                         name=u'unique_package'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


    def __init__(self, pkg_def_id, pkg_name, version, revision, created,
                 creator, builder, project_type):
        """ """

        self.pkg_def_id = pkg_def_id
        self.pkg_name = pkg_name
        self.version = version
        self.revision = revision
        self.created = created
        self.creator = creator
        self.builder = builder
        self.project_type = project_type


class Projects(Base):
    __tablename__ = 'projects'

    id = Column(u'project_id', INTEGER(), primary_key=True)
    name = Column(VARCHAR(length=255), nullable=False, unique=True)


    def __init__(self, name):
        """ """

        self.name = name


class Zones(Base):
    __tablename__ = 'zones'

    id = Column(u'ZoneID', INTEGER(), primary_key=True)
    zone_name = Column(u'zoneName',VARCHAR(length=30))
    mx_priority = Column(u'mxPriority', INTEGER())
    mx_host_id = Column(u'mxHostID', VARCHAR(length=30))
    ns_priority = Column(u'nsPriority', INTEGER())
    nameserver = Column(VARCHAR(length=30))


    def __init__(self, zone_name, mx_priority, mx_host_id, ns_priority,
                 nameserver):
        """ """

        self.zone_name = zone_name
        self.mx_priority = mx_priority
        self.mx_host_id = mx_host_id
        self.ns_priority = ns_priority
        self.nameserver = nameserver


class Deployments(Base):
    __tablename__ = 'deployments'

    id = Column(u'DeploymentID', INTEGER(), primary_key=True)
    package_id = Column(INTEGER(),
                        ForeignKey(Packages.id, ondelete='cascade'),
                        nullable=False)
    user = Column(VARCHAR(length=32), nullable=False)
    dep_type = Column(Enum('deploy', 'rollback'), nullable=False)
    declared = Column(TIMESTAMP(), nullable=False,
                      default=func.current_timestamp(),
                      server_default=func.current_timestamp())


    def __init__(self, package_id, user, dep_type, declared):
        """ """

        self.package_id = package_id
        self.user = user
        self.dep_type = dep_type
        self.declared = declared


class NagCommandArguments(Base):
    __tablename__ = 'nag_command_arguments'

    id = Column(INTEGER(), primary_key=True)
    check_command_id = Column(INTEGER(),
                              ForeignKey(NagCheckCommands.id,
                                         ondelete='cascade'),
                              nullable=False)
    label = Column(VARCHAR(length=32), nullable=False)
    description = Column(VARCHAR(length=255), nullable=False)
    arg_order = Column(INTEGER(), nullable=False)
    default_value = Column(VARCHAR(length=80))

    __table_args__ = (
        UniqueConstraint(u'check_command_id', u'arg_order',
                         name='check_command_arg_order'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


nag_contact_groups_members = Table(u'nag_contact_groups_members',
    Base.metadata,
    Column(u'contact_id', INTEGER(),
           ForeignKey(NagContacts.id, ondelete='cascade'),
           primary_key=True),
    Column(u'contact_group_id', INTEGER(),
           ForeignKey(NagContactGroups.id, ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)


class NagServices(Base):
    __tablename__ = 'nag_services'

    id = Column(INTEGER(), primary_key=True)
    check_command_id = Column(INTEGER(),
                              ForeignKey(NagCheckCommands.id,
                                         ondelete='cascade'),
                              nullable=False)
    description = Column(VARCHAR(length=255), nullable=False)
    max_check_attempts = Column(INTEGER(), nullable=False)
    check_interval = Column(INTEGER(), nullable=False)
    check_period_id = Column(INTEGER(),
                             ForeignKey(NagTimePeriods.id,
                                        ondelete='cascade'),
                             nullable=False)
    retry_interval = Column(INTEGER(), nullable=False)
    notification_interval = Column(INTEGER(), nullable=False)
    notification_period_id = Column(INTEGER(),
                                    ForeignKey(NagTimePeriods.id,
                                               ondelete='cascade'),
                                    nullable=False)


ns_service_binds = Table(u'ns_service_binds', Base.metadata,
    Column(u'serviceID', INTEGER(unsigned=True),
           ForeignKey(NsService.id, ondelete='cascade'),
           primary_key=True),
    Column(u'monitorID', INTEGER(unsigned=True),
           ForeignKey(NsMonitor.id, ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)


class NsServiceMax(Base):
    __tablename__ = 'ns_service_max'

    spec_id = Column(u'specID', INTEGER(),
                     ForeignKey(HostSpecs.id, ondelete='cascade'),
                     primary_key=True)
    service_id = Column(u'serviceID', INTEGER(unsigned=True),
                        ForeignKey(NsService.id, ondelete='cascade'),
                        primary_key=True)
    max_client = Column(u'maxClient', INTEGER(unsigned=True), nullable=False,
                        default=0, server_default='0')
    max_requests = Column(u'maxReq', INTEGER(unsigned=True), nullable=False,
                          default=0, server_default='0')


    def __init__(self, spec_id, service_id, max_client, max_requests):
        """ """

        self.spec_id = spec_id
        self.service_id = service_id
        self.max_client = max_client
        self.max_requests = max_requests


class NsServiceParams(Base):
    __tablename__ = 'ns_service_params'

    service_id = Column(u'serviceID', INTEGER(unsigned=True),
                        ForeignKey(NsService.id, ondelete='cascade'),
                        primary_key=True)
    param = Column(VARCHAR(length=32), primary_key=True)
    value = Column(VARCHAR(length=128), nullable=False)


    def __init__(self, service_id, param, value):
        """ """

        self.service_id = service_id
        self.param = param
        self.value = value


class NsVip(Base):
    __tablename__ = 'ns_vip'

    id = Column(u'vipID', INTEGER(unsigned=True), primary_key=True)
    vserver = Column(VARCHAR(length=64), nullable=False)
    device_id = Column(u'deviceID', INTEGER(unsigned=True),
                       ForeignKey(NsDevice.id, ondelete='cascade'),
                       nullable=False)

    __table_args__ = (
        UniqueConstraint(u'deviceID', u'vserver', name=u'device_vserver'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


    def __init__(self, vserver, device_id):
        """ """

        self.vserver = vserver
        self.device_id = device_id


class PackageNames(Base):
    __tablename__ = 'package_names'

    id = Column(u'pkg_name_id', INTEGER(), primary_key=True)
    name = Column(VARCHAR(length=255), nullable=False)
    pkg_def_id = Column(INTEGER(),
                        ForeignKey(PackageDefinitions.id, ondelete='cascade'),
                        nullable=False)

    __table_args__ = (
        UniqueConstraint(u'name', u'pkg_def_id', name='name_pkg_def_id'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )

    def __init__(self, name, pkg_def_id=None):
        """ """

        self.name = name
        self.pkg_def_id = pkg_def_id


class Ports(Base):
    __tablename__ = 'ports'

    id = Column(u'PortID', INTEGER(), primary_key=True)
    network_id = Column(u'NetworkID', INTEGER(),
                        ForeignKey(NetworkDevice.id, ondelete='cascade'))
    port_number = Column(u'portNumber', VARCHAR(length=20))
    description = Column(VARCHAR(length=50))
    speed = Column(VARCHAR(length=20))
    duplex = Column(VARCHAR(length=20))

    __table_args__ = (
        UniqueConstraint('NetworkID', 'portNumber',
                         name='NetworkID_portNumber'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


    def __init__(self, network_id, port_number, description, speed, duplex):
        """ """

        self.network_id = network_id
        self.port_number = port_number
        self.description = description
        self.speed = speed
        self.duplex = duplex


class Vlans(Base):
    __tablename__ = 'vlans'

    id = Column(u'VlanID', INTEGER(), primary_key=True)
    name = Column(VARCHAR(length=20))
    environment_id = Column(u'environmentID', INTEGER(),
                            ForeignKey(Environments.id, ondelete='cascade'))
    description = Column(VARCHAR(length=50))


    def __init__(self, name, description):
        """ """

        self.name = name
        self.description = description


class AppDefinitions(Base):
    __tablename__ = 'app_definitions'

    id = Column(u'AppID', SMALLINT(display_width=2), primary_key=True)
    production_vlan_id = Column(u'Production_VlanID', INTEGER(),
                                ForeignKey(Vlans.id), nullable=False)
    development_vlan_id = Column(u'Development_VlanID', INTEGER(),
                                 ForeignKey(Vlans.id), nullable=False)
    staging_vlan_id = Column(u'Staging_VlanID', INTEGER(),
                             ForeignKey(Vlans.id), nullable=False)
    distribution = Column(Enum(u'co54', u'co62', u'co64', u'rh53', u'rh62',
                               u'rh63', u'rh64'), nullable=False,
                          default='co64', server_default='co64')
    app_type = Column(u'appType', VARCHAR(length=100), nullable=False)
    host_base = Column(u'hostBase', VARCHAR(length=100))
    puppet_class = Column(u'puppetClass', VARCHAR(length=100), nullable=False,
                          default='baseclass', server_default='baseclass')
    ganglia_id = Column(u'GangliaID', INTEGER(), ForeignKey(Ganglia.id),
                        nullable=False, default=1, server_default='1')
    ganglia_group_name = Column(u'GgroupName', VARCHAR(length=25))
    description = Column(VARCHAR(length=100))
    status = Column(Enum('active', 'inactive'), nullable=False,
                    default='active', server_default='active')


    def __init__(self, production_vlan_id, development_vlan_id,
                 staging_vlan_id, distribution, app_type, host_base,
                 puppet_class, ganglia_id, ganglia_group_name,
                 description, status):
        """ """

        self.production_vlan_id = production_vlan_id
        self.development_vlan_id = development_vlan_id
        self.staging_vlan_id = staging_vlan_id
        self.distribution = distribution
        self.app_type = app_type
        self.host_base = host_base
        self.puppet_class = puppet_class
        self.ganglia_id = ganglia_id
        self.ganglia_group_name = ganglia_group_name
        self.description = description
        self.status = status


class NagServicesArguments(Base):
    __tablename__ = 'nag_services_arguments'

    service_id = Column(INTEGER(),
                        ForeignKey(NagServices.id, ondelete='cascade'),
                        primary_key=True)
    command_argument_id = Column(INTEGER(),
                                 ForeignKey(NagCommandArguments.id,
                                            ondelete='cascade'),
                                 primary_key=True)
    value = Column(VARCHAR(length=120), nullable=False)


nag_services_contact_groups = Table(u'nag_services_contact_groups',
    Base.metadata,
    Column(u'service_id', INTEGER(),
           ForeignKey(NagServices.id, ondelete='cascade'),
           primary_key=True),
    Column(u'contact_group_id', INTEGER(),
           ForeignKey(NagContactGroups.id, ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)

nag_services_contacts = Table(u'nag_services_contacts', Base.metadata,
    Column(u'service_id', INTEGER(),
           ForeignKey(NagServices.id, ondelete='cascade'),
           primary_key=True),
    Column(u'contact_id', INTEGER(),
           ForeignKey(NagContacts.id, ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)


class NsWeight(Base):
    __tablename__ = 'ns_weight'

    vip_id = Column(u'vipID', INTEGER(unsigned=True),
                    ForeignKey(NsVip.id, ondelete='cascade'),
                    primary_key=True)
    spec_id = Column(u'specID', INTEGER(),
                     ForeignKey(HostSpecs.id, ondelete='cascade'),
                     primary_key=True)
    weight = Column(TINYINT(display_width=3, unsigned=True), nullable=False)


    def __init__(self, vip_id, spec_id, weight):
        """ """

        self.vip_id = vip_id
        self.spec_id = spec_id
        self.weight = weight


class Subnet(Base):
    __tablename__ = 'subnet'

    id = Column(u'SubnetID', INTEGER(), primary_key=True)
    vlan_id = Column(u'VlanID', INTEGER(),
                     ForeignKey(Vlans.id, ondelete='cascade'))
    ip_address = Column(u'ipAddress', VARCHAR(length=15), unique=True)
    netmask = Column(VARCHAR(length=15))
    gateway = Column(VARCHAR(length=15))
    zone_id = Column(u'ZoneID', INTEGER(), ForeignKey(Zones.id))


    def __init__(self, vlan_id, ip_address, netmask, gateway, zone_id):
        """ """

        self.vlan_id = vlan_id
        self.ip_address = ip_address
        self.netmask = netmask
        self.gateway = gateway
        self.zone_id = zone_id


class AppDeployments(Base):
    __tablename__ = 'app_deployments'

    id = Column(u'AppDeploymentID', INTEGER(), primary_key=True)
    deployment_id = Column(u'DeploymentID', INTEGER(),
                           ForeignKey(Deployments.id, ondelete='cascade'),
                           nullable=False)
    app_id = Column(u'AppID', SMALLINT(display_width=6),
                    ForeignKey(AppDefinitions.id, ondelete='cascade'),
                    nullable=False)
    user = Column(VARCHAR(length=32), nullable=False)
    status = Column(Enum('complete', 'incomplete', 'inprogress',
                         'invalidated', 'validated'),
                    nullable=False)
    environment = Column(VARCHAR(length=15), nullable=False)
    realized = Column(TIMESTAMP(), nullable=False,
                      default=func.current_timestamp(),
                      server_default=func.current_timestamp())


    def __init__(self, deployment_id, app_id, user, status, environment,
                 realized):
        """ """

        self.deployment_id = deployment_id
        self.app_id = app_id
        self.user = user
        self.status = status
        self.environment = environment
        self.realized = realized


app_hipchat_rooms = Table(u'app_hipchat_rooms', Base.metadata,
    Column(u'AppID', SMALLINT(display_width=6),
           ForeignKey(AppDefinitions.id, ondelete='cascade'),
           primary_key=True),
    Column(u'roomID', INTEGER(), ForeignKey(Hipchat.id, ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)


app_jmx_attributes = Table(u'app_jmx_attributes', Base.metadata,
    Column(u'AppID', SMALLINT(display_width=6),
           ForeignKey(AppDefinitions.id, ondelete='cascade'),
           primary_key=True),
    Column(u'jmx_attribute_id', INTEGER(),
           ForeignKey(JmxAttributes.id, ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)


app_packages = Table(u'app_packages', Base.metadata,
    Column(u'pkgLocationID', INTEGER(),
           ForeignKey(PackageLocations.id, ondelete='cascade'),
           primary_key=True),
    Column(u'AppID', SMALLINT(display_width=6),
           ForeignKey(AppDefinitions.id, ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)


class DefaultSpecs(Base):
    __tablename__ = 'default_specs'

    spec_id = Column(u'specID', INTEGER(),
                     ForeignKey(HostSpecs.id, ondelete='cascade'),
                     primary_key=True)
    app_id = Column(u'AppID', SMALLINT(display_width=6),
                    ForeignKey(AppDefinitions.id, ondelete='cascade'),
                    primary_key=True)
    environment_id = Column(u'environmentID', INTEGER(),
                            ForeignKey(Environments.id, ondelete='cascade'),
                            primary_key=True)
    priority = Column(INTEGER(display_width=4), nullable=False, default='10',
                      server_default='10')


    def __init__(self, spec_id, app_id, environment_id, priority):
        """ """

        self.spec_id = spec_id
        self.app_id = app_id
        self.environment_id = environment_id
        self.priority = priority


class Hosts(Base):
    __tablename__ = 'hosts'

    id = Column(u'HostID', INTEGER(), primary_key=True)
    spec_id = Column(u'SpecID', INTEGER(), ForeignKey(HostSpecs.id))
    state = Column(Enum(u'baremetal', u'operational', u'repair', u'parts',
                   u'reserved', u'escrow'), nullable=False)
    hostname = Column(VARCHAR(length=30))
    arch = Column(VARCHAR(length=10))
    kernel_version = Column(u'kernelVersion', VARCHAR(length=20))
    distribution = Column(VARCHAR(length=20))
    timezone = Column(VARCHAR(length=10))
    app_id = Column(u'AppID', SMALLINT(display_width=6),
                    ForeignKey(AppDefinitions.id), nullable=False)
    cage_location = Column(u'cageLocation', INTEGER())
    cab_location = Column(u'cabLocation', VARCHAR(length=10))
    section = Column(VARCHAR(length=10))
    rack_location = Column(u'rackLocation', INTEGER())
    console_port = Column(u'consolePort', VARCHAR(length=11))
    power_port = Column(u'powerPort', VARCHAR(length=10))
    power_circuit = Column(u'powerCircuit', VARCHAR(length=10))
    environment = Column(VARCHAR(length=15))

    __table_args__ = (
        UniqueConstraint(u'cageLocation', u'cabLocation', u'consolePort'),
        UniqueConstraint(u'cageLocation', u'cabLocation', u'rackLocation'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
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


class NagApptypesServices(Base):
    __tablename__ = 'nag_apptypes_services'

    app_id = Column(SMALLINT(display_width=2),
                    ForeignKey(AppDefinitions.id, ondelete='cascade'),
                    primary_key=True)
    service_id = Column(INTEGER(),
                        ForeignKey(NagServices.id, ondelete='cascade'),
                        primary_key=True)
    server_app_id = Column(SMALLINT(display_width=6),
                           ForeignKey(AppDefinitions.id),
                           primary_key=True)
    environment_id = Column(INTEGER(),
                            ForeignKey(Environments.id, ondelete='cascade'),
                            primary_key=True)


class NsVipBinds(Base):
    __tablename__ = 'ns_vip_binds'

    app_id = Column(u'appID', SMALLINT(display_width=6),
                    ForeignKey(AppDefinitions.id, ondelete='cascade'),
                    primary_key=True)
    vip_id = Column(u'vipID', INTEGER(unsigned=True),
                    ForeignKey(NsVip.id, ondelete='cascade'),
                    primary_key=True)
    service_id = Column(u'serviceID', INTEGER(unsigned=True),
                        ForeignKey(NsService.id, ondelete='cascade'),
                        primary_key=True)
    environment_id = Column(u'environmentID', INTEGER(),
                            ForeignKey(Environments.id, ondelete='cascade'),
                            primary_key=True)


class ProjectPackage(Base):
    __tablename__ = 'project_package'

    project_id = Column(INTEGER(),
                        ForeignKey(Projects.id, ondelete='cascade'),
                        primary_key=True)
    pkg_def_id = Column(INTEGER(),
                        ForeignKey(PackageDefinitions.id, ondelete='cascade'),
                        primary_key=True)
    app_id = Column(SMALLINT(display_width=6),
                    ForeignKey(AppDefinitions.id, ondelete='cascade'),
                    primary_key=True)


class Asset(Base):
    __tablename__ = 'asset'

    id = Column(u'AssetID', INTEGER(), primary_key=True)
    host_id = Column(u'HostID', INTEGER(),
                     ForeignKey(Hosts.id, ondelete='cascade'),
                     nullable=False)
    date_received = Column(u'dateReceived', DATE())
    description = Column(VARCHAR(length=20))
    oem_serial = Column(u'oemSerial', VARCHAR(length=30), unique=True)
    service_tag = Column(u'serviceTag', VARCHAR(length=20))
    tagged_serial = Column(u'taggedSerial', VARCHAR(length=20))
    invoice_number = Column(u'invoiceNumber', VARCHAR(length=20))
    location_site = Column(u'locationSite', VARCHAR(length=20))
    location_owner = Column(u'locationOwner', VARCHAR(length=20))
    cost_per_item = Column(u'costPerItem', VARCHAR(length=20))
    date_of_invoice = Column(u'dateOfInvoice', DATE())
    warranty_start = Column(u'warrantyStart', DATE())
    warranty_end = Column(u'warrantyEnd', DATE())
    warranty_level = Column(u'warrantyLevel', VARCHAR(length=20))
    warranty_id = Column(u'warrantyID', VARCHAR(length=20))
    vendor_contact = Column(u'vendorContact', VARCHAR(length=20))


    def __init__(self, host_id, date_received, description, oem_serial,
                 service_tag, tagged_serial, invoice_number, location_site,
                 location_owner, cost_per_item, date_of_invoice,
                 warranty_start, warranty_end, warranty_level, warranty_id,
                 vendor_contact):
        """ """

        self.host_id = host_id
        self.date_received = date_received
        self.description = description
        self.oem_serial = oem_serial
        self.service_tag = service_tag
        self.tagged_serial = tagged_serial
        self.invoice_number = invoice_number
        self.location_site = location_site
        self.location_owner = location_owner
        self.cost_per_item = cost_per_item
        self.date_of_invoice = date_of_invoice
        self.warranty_start = warranty_start
        self.warranty_end = warranty_end
        self.warranty_level = warranty_level
        self.warranty_id = warranty_id
        self.vendor_contact = vendor_contact


class HostDeployments(Base):
    __tablename__ = 'host_deployments'

    id = Column(u'HostDeploymentID', INTEGER(), primary_key=True)
    deployment_id = Column(u'DeploymentID', INTEGER(),
                           ForeignKey(Deployments.id, ondelete='cascade'),
                           nullable=False)
    host_id = Column(u'HostID', INTEGER(),
                     ForeignKey(Hosts.id, ondelete='cascade'),
                     nullable=False)
    user = Column(VARCHAR(length=32), nullable=False)
    status = Column(Enum('inprogress', 'failed', 'ok'), nullable=False)
    realized = Column(TIMESTAMP(), nullable=False,
                      default=func.current_timestamp(),
                      server_default=func.current_timestamp())


    def __init__(self, deployment_id, host_id, user, status, realized):
        """ """

        self.deployment_id = deployment_id
        self.host_id = host_id
        self.user = user
        self.status = status
        self.realized = realized


class HostInterfaces(Base):
    __tablename__ = 'host_interfaces'

    id = Column(u'InterfaceID', INTEGER(), primary_key=True)
    host_id = Column(u'HostID', INTEGER(),
                     ForeignKey(Hosts.id, ondelete='cascade'),
                     index=True)
    network_id = Column(u'NetworkID', INTEGER(),
                        ForeignKey(NetworkDevice.id, ondelete='cascade'),
                        index = True)
    interface_name = Column(u'interfaceName', VARCHAR(length=10))
    mac_address = Column(u'macAddress', VARCHAR(length=18), unique=True)
    port_id = Column(u'PortID', INTEGER(), ForeignKey(Ports.id),
                     unique=True, index=True)

    __table_args__ = (
        UniqueConstraint(u'HostID', u'interfaceName'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


    def __init__(self, host_id, network_id, interface_name, mac_address,
                 port_id):
        """ """

        self.host_id = host_id
        self.network_id = network_id
        self.interface_name = interface_name
        self.mac_address = mac_address
        self.port_id = port_id


class Iloms(Base):
    __tablename__ = 'iloms'

    id = Column(u'ILomID', INTEGER(), primary_key=True)
    host_id = Column(u'HostID', INTEGER(),
                     ForeignKey(Hosts.id, ondelete='cascade'),
                     unique=True, index=True)
    subnet_id = Column(u'SubnetID', INTEGER(),
                       ForeignKey(Subnet.id, ondelete='cascade'),
                       nullable=False, unique=True, index=True)
    mac_address = Column(u'macAddress', VARCHAR(length=18), unique=True)
    port_id = Column(u'PortID', INTEGER(),
                     ForeignKey(Ports.id, ondelete='cascade'),
                     unique=True, index=True)
    a_record = Column(u'ARecord', VARCHAR(length=200))
    comments = Column(VARCHAR(length=200))


    def __init__(self, host_id, subnet_id, mac_address, port_id, a_record,
                 comments):
        """ """

        self.host_id = host_id
        self.subnet_id = subnet_id
        self.mac_address = mac_address
        self.port_id = port_id
        self.a_record = a_record
        self.comments = comments


class NagHostsServices(Base):
    __tablename__ = 'nag_hosts_services'

    host_id = Column(INTEGER(), ForeignKey(Hosts.id, ondelete='cascade'),
                     primary_key=True)
    service_id = Column(INTEGER(),
                        ForeignKey(NagServices.id, ondelete='cascade'),
                        primary_key=True)
    server_app_id = Column(SMALLINT(display_width=6),
                           ForeignKey(AppDefinitions.id),
                           primary_key=True)


class ServiceEvent(Base):
    __tablename__ = 'serviceEvent'

    id = Column(u'ServiceID', INTEGER(), primary_key=True)
    host_id = Column(u'HostID', INTEGER(),
                     ForeignKey(Hosts.id, ondelete='cascade'))
    user = Column(VARCHAR(length=20))
    service_status = Column(u'serviceStatus', VARCHAR(length=100))
    power_status = Column(u'powerStatus', VARCHAR(length=10))
    vendor_ticket = Column(u'vendorTicket', VARCHAR(length=20))
    comments = Column(TEXT())
    service_date = Column(u'serviceDate', TIMESTAMP(), nullable=False,
                          default=func.current_timestamp(),
                          onupdate=func.current_timestamp(),
                          server_onupdate=func.current_timestamp())


    def __init__(self, host_id, user, service_status, power_status,
                 vendor_ticket, comments, service_date):
        """ """

        self.host_id = host_id
        self.user = user
        self.service_status = service_status
        self.power_status = power_status
        self.vendor_ticket = vendor_ticket
        self.comments = comments
        self.service_date = service_date


class HostIps(Base):
    __tablename__ = 'host_ips'

    id = Column(u'IpID', INTEGER(), primary_key=True)
    interface_id = Column(u'InterfaceID', INTEGER(),
                          ForeignKey(HostInterfaces.id, ondelete='cascade'),
                          nullable=False, index=True)
    subnet_id = Column(u'SubnetID', INTEGER(),
                       ForeignKey(Subnet.id, ondelete='cascade'),
                       nullable=False, unique=True, index=True)
    priority = Column(INTEGER(unsigned=True), nullable=False, default=1,
                      server_default='1')
    a_record = Column(u'ARecord', VARCHAR(length=200))
    comments = Column(VARCHAR(length=200))


    def __init__(self, interface_id, subnet_id, priority, a_record, comments):
        """ """

        self.interface_id = interface_id
        self.subnet_id = subnet_id
        self.priority = priority
        self.a_record = a_record
        self.comments = comments


class Cname(Base):
    __tablename__ = 'cname'

    id = Column(u'CnameID', INTEGER(), primary_key=True)
    name = Column(VARCHAR(length=40))
    ip_id = Column(u'IpID', INTEGER(),
                   ForeignKey(HostIps.id, onupdate='cascade',
                              ondelete='cascade'))
    zone_id = Column(u'ZoneID', INTEGER(),
                     ForeignKey(Zones.id, onupdate='cascade',
                                ondelete='cascade'))

    __table_args__ = (
        UniqueConstraint(u'name', u'ZoneID', name=u'name_ZoneID'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )


    def __init__(self, name, ip_id, zone_id):
        """ """

        self.name = name
        self.ip_id = ip_id
        self.zone_id = zone_id


#
# Relationships
#


Environments.host_specs = relationship(DefaultSpecs)
Environments.ns_services = relationship(NsVipBinds)
Environments.ns_vips = relationship(NsVipBinds)

Ganglia.app_definitions = relationship(AppDefinitions)

HostSpecs.services = relationship(NsServiceMax)

NagCheckCommands.nag_command_arguments = relationship(NagCommandArguments)

NagContactGroups.nag_contacts = \
    relationship(NagContacts, secondary=nag_contact_groups_members,
                 backref='nag_contact_groups')

NetworkDevice.host_interface = relationship(HostInterfaces, uselist=False)
NetworkDevice.ports = relationship(Ports)

NsDevice.vips = relationship(NsVip)

NsService.ns_monitors = relationship(NsMonitor, secondary=ns_service_binds)
NsService.service_params = relationship(NsServiceParams)

PackageDefinitions.packages = relationship(Packages,
                                           backref='package_definition')
PackageDefinitions.package_names = relationship(PackageNames)
PackageDefinitions.proj_pkg = relationship(ProjectPackage)

PackageLocations.app_definitions = relationship(AppDefinitions,
                                                secondary=app_packages,
                                                backref='package_locations')

Packages.deployments = relationship(Deployments)

Projects.proj_pkg = relationship(ProjectPackage)

Zones.cnames = relationship(Cname, backref='zone')

Deployments.app_deployments = relationship(AppDeployments)
Deployments.host_deployments = relationship(HostDeployments)

NagServices.applications = relationship(NagApptypesServices)
NagServices.check_period = \
    relationship(NagTimePeriods, foreign_keys=[ NagServices.check_period_id ],
                 uselist=False)
NagServices.command_arguments = relationship(NagServicesArguments,
                                             backref='nag_services')
NagServices.contact_groups = \
    relationship(NagContactGroups, secondary=nag_services_contact_groups,
                 backref='nag_services')
NagServices.contacts = \
    relationship(NagContacts, secondary=nag_services_contacts,
                 backref='nag_services')
NagServices.environments = relationship(NagApptypesServices)
NagServices.hosts = relationship(NagHostsServices)
NagServices.nag_check_command = relationship(NagCheckCommands, uselist=False,
                                             backref='nag_services')
NagServices.notification_period = \
    relationship(NagTimePeriods,
                 foreign_keys=[ NagServices.notification_period_id ],
                 uselist=False)

NsServiceMax.service = relationship(NsService, uselist=False)

NsVip.host_specs = relationship(NsWeight, backref='ns_vip')

Ports.network_interface = relationship(HostInterfaces, uselist=False)

Vlans.subnets = relationship(Subnet)

AppDefinitions.app_deployments = relationship(AppDeployments)
AppDefinitions.hipchats = relationship(Hipchat, secondary=app_hipchat_rooms,
                                       backref='app_definitions')
AppDefinitions.hosts = relationship(Hosts)
AppDefinitions.host_specs = relationship(DefaultSpecs)
AppDefinitions.ns_services = relationship(NsVipBinds)
AppDefinitions.nag_app_services = \
    relationship(NagApptypesServices,
                 primaryjoin=NagApptypesServices.app_id == AppDefinitions.id)
AppDefinitions.nag_host_services = relationship(NagHostsServices)
AppDefinitions.proj_pkg = relationship(ProjectPackage)
AppDefinitions.development_vlans = \
    relationship(Vlans, foreign_keys=[ AppDefinitions.development_vlan_id ])
AppDefinitions.production_vlans = \
    relationship(Vlans, foreign_keys=[ AppDefinitions.production_vlan_id ])
AppDefinitions.staging_vlans = \
    relationship(Vlans, foreign_keys=[ AppDefinitions.staging_vlan_id ])

NagServicesArguments.command_argument = \
    relationship(NagCommandArguments, backref='nag_services_assoc')

NsWeight.host_spec = relationship(NsVip, uselist=False,
                                  backref='ns_vip_assocs')

Subnet.zone = relationship(Zones, uselist=False, backref='subnets')

DefaultSpecs.host_spec = relationship(HostSpecs, uselist=False)

Hosts.host_deployments = relationship(HostDeployments)
Hosts.host_interfaces = relationship(HostInterfaces, backref='host')
Hosts.host_spec = relationship(HostSpecs, uselist=False, backref='hosts')
Hosts.ilom = relationship(Iloms, uselist=False, backref='host')
Hosts.service_events = relationship(ServiceEvent, backref='host')

NagApptypesServices.application = \
    relationship(AppDefinitions, foreign_keys=[ NagApptypesServices.app_id ])
NagApptypesServices.environment = relationship(Environments)
NagApptypesServices.service = relationship(NagServices)

NsVipBinds.ns_service = relationship(NsService)
NsVipBinds.ns_vip = relationship(NsVip)

ProjectPackage.app_definitions = relationship(AppDefinitions)
ProjectPackage.package_definitions = relationship(PackageDefinitions)
ProjectPackage.projects = relationship(Projects)

Asset.host = relationship(Hosts, uselist=False)

HostInterfaces.host_ips = relationship(HostIps, backref='host_interface')

Iloms.port = relationship(Subnet, uselist=False, backref='port')
Iloms.subnet = relationship(Subnet, uselist=False, backref='ilom')

NagHostsServices.host = relationship(Hosts)
NagHostsServices.service = relationship(NagServices)

HostIps.subnet = relationship(Subnet, uselist=False, backref='host_ip')

Cname.host = relationship(HostIps, uselist=False)
