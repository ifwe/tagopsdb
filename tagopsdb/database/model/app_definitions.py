from elixir import Field
from elixir import String, Enum
from elixir import using_options, belongs_to, has_and_belongs_to_many
from sqlalchemy.dialects.mysql import SMALLINT

from .base import Base


class AppDefinitions(Base):
    using_options(tablename='app_definitions')

    id = Field(SMALLINT(display_width=2), colname='AppID', primary_key=True)

    distribution = Field(
        Enum('co54', 'co62', 'co64', 'co65', 'rh53', 'rh62', 'rh63', 'rh64'),
        default='co64',
        server_default='co64'
    )

    app_type = Field(String(length=100), colname='appType', nullable=False)
    host_base = Field(String(length=100), colname='hostBase')
    puppet_class = Field(
        String(length=100),
        colname='puppetClass',
        nullable=False,
        default='baseclass',
        server_default='baseclass'
    )

    ganglia_group_name = Field(String(length=25), colname='GgroupName')
    description = Field(String(length=100))
    status = Field(
        Enum('active', 'inactive'),
        nullable=False,
        default='active',
        server_default='active'
    )

    belongs_to(
        'ganglia',
        of_kind='Ganglia',
        colname='GangliaID',
    )
    belongs_to(
        'production_vlan',
        of_kind='Vlans',
        colname='Production_VlanID'
    )
    belongs_to(
        'staging_vlan',
        of_kind='Vlans',
        colname='Staging_VlanID'
    )
    belongs_to(
        'development_vlan',
        of_kind='Vlans',
        colname='Development_VlanID'
    )

    has_and_belongs_to_many(
        'projects',
        of_kind='Projects',
        inverse='app_definitions',
        tablename='project_package',
        local_colname='app_id',
        remote_colname='project_id',
        table_kwargs=dict(extend_existing=True)
    )

    has_and_belongs_to_many(
        'packages',
        of_kind='PackageDefinitions',
        inverse='app_definitions',
        tablename='project_package',
        local_colname='app_id',
        remote_colname='pkg_def_id',
        table_kwargs=dict(extend_existing=True)
    )

    # app_deployments = relationship('AppDeployments')
    # hipchats = relationship(
    #     'Hipchat',
    #     secondary='app_hipchat_rooms',
    #     backref='app_definitions'
    # )
    # hosts = relationship('Hosts')
    # host_specs = relationship('DefaultSpecs')
    # ns_services = relationship('NsVipBinds')
    # nag_app_services = relationship(
    #     'NagApptypesServices',
    #     primaryjoin='NagApptypesServices.app_id == AppDefinitions.id'
    # )
    # nag_host_services = relationship('NagHostsServices')
    # proj_pkg = relationship('ProjectPackage')
