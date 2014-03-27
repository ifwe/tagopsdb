from elixir import Field
from elixir import String, Enum
from elixir import using_options, using_table_options
from elixir import belongs_to, has_and_belongs_to_many, has_many
from sqlalchemy.dialects.mysql import SMALLINT

from .base import Base


class Application(Base):
    using_options(tablename='app_definitions')
    using_table_options(extend_existing=True)

    id = Field(SMALLINT(display_width=2), colname='AppID', primary_key=True)

    distribution = Field(
        Enum('co54', 'co62', 'co64', 'co65', 'rh53', 'rh62', 'rh63', 'rh64'),
        required=True,
        default='co64',
        server_default='co64'
    )

    name = Field(
        String(length=100),
        colname='appType',
        required=True
    )
    host_base = Field(String(length=100), colname='hostBase')
    puppet_class = Field(
        String(length=100),
        colname='puppetClass',
        required=True,
        default='baseclass',
        server_default='baseclass'
    )

    ganglia_group_name = Field(
        String(length=25),
        colname='GgroupName',
        required=True
    )
    description = Field(String(length=100))
    status = Field(
        Enum('active', 'inactive'),
        required=True,
        default='active',
        server_default='active'
    )

    belongs_to(
        'ganglia',
        of_kind='Ganglia',
        colname='GangliaID',
        required=True,
    )
    belongs_to(
        'production_vlan',
        of_kind='Vlans',
        colname='Production_VlanID',
        required=True
    )
    belongs_to(
        'staging_vlan',
        of_kind='Vlans',
        colname='Staging_VlanID',
        required=True,
    )
    belongs_to(
        'development_vlan',
        of_kind='Vlans',
        colname='Development_VlanID',
        required=True
    )

    has_and_belongs_to_many(
        'projects',
        of_kind='Projects',
        inverse='apps',
        tablename='project_package',
        local_colname='app_id',
        remote_colname='project_id',
        table_kwargs=dict(extend_existing=True)
    )

    has_and_belongs_to_many(
        'packages',
        of_kind='PackageDefinitions',
        inverse='apps',
        tablename='project_package',
        local_colname='app_id',
        remote_colname='pkg_def_id',
        table_kwargs=dict(extend_existing=True)
    )

    has_many(
        'app_deployments',
        of_kind='AppDeployment',
        inverse='app'
    )

    has_and_belongs_to_many(
        'hipchat_rooms',
        of_kind='Hipchat',
        inverse='apps',
        tablename='app_hipchat_rooms',
        local_colname='AppID',
        remote_colname='roomID',
        table_kwargs=dict(extend_existing=True)
    )

    has_and_belongs_to_many(
        'jmx_attributes',
        of_kind='JmxAttribute',
        inverse='apps',
        tablename='app_jmx_attributes',
        local_colname='AppID',
        remote_colname='jmx_attribute_id',
        table_kwargs=dict(extend_existing=True),
    )

    has_and_belongs_to_many(
        'package_locations',
        of_kind='PackageLocations',
        inverse='apps',
        tablename='app_packages',
        local_colname='AppID',
        remote_colname='pkgLocationID',
        table_kwargs=dict(extend_existing=True),
    )

    has_many(
        'default_specs',
        of_kind='DefaultSpec',
        inverse='app'
    )

    has_many(
        'hosts',
        of_kind='Host',
        inverse='app',
    )

    # app_deployments = relationship('AppDeployment')
    # hipchats = relationship(
    #     'Hipchat',
    #     secondary='app_hipchat_rooms',
    #     backref='app_definitions'
    # )
    # hosts = relationship('Host')
    # host_specs = relationship('DefaultSpec')
    # ns_services = relationship('NsVipBinds')
    # nag_app_services = relationship(
    #     'NagApptypesServices',
    #     primaryjoin='NagApptypesServices.app_id == Application.id'
    # )
    # nag_host_services = relationship('NagHostServices')
    # proj_pkg = relationship('ProjectPackage')
