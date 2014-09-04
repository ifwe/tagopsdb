from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship, synonym

from .meta import Base, Column, String


class AppDefinition(Base):
    __tablename__ = 'app_definitions'

    dummy = '__dummy__'

    id = Column(u'AppID', SMALLINT(display_width=2), primary_key=True)
    distribution = Column(
        Enum(
            u'centos5.4', u'centos6.2', u'centos6.4', u'centos6.5',
            u'rhel5.3', u'rhel6.2', u'rhel6.3', u'rhel6.4', u'rhel6.5',
        ),
        nullable=False,
        server_default='centos6.4'
    )
    app_type = Column(u'appType', String(length=100), nullable=False)
    name = synonym('app_type')
    host_base = Column(u'hostBase', String(length=100))
    puppet_class = Column(
        u'puppetClass',
        String(length=100),
        nullable=False,
        server_default='baseclass'
    )
    ganglia_id = Column(
        u'GangliaID',
        INTEGER(),
        ForeignKey('ganglia.GangliaID'),
        nullable=False,
        server_default='1'
    )
    ganglia_group_name = Column(u'GgroupName', String(length=25))
    description = Column(String(length=100))
    status = Column(
        Enum('active', 'inactive'),
        nullable=False,
        server_default='active'
    )
    app_deployments = relationship('AppDeployment', order_by="AppDeployment.created_at, AppDeployment.id")
    hipchats = relationship(
        'Hipchat',
        secondary='app_hipchat_rooms',
        back_populates='app_definitions'
    )
    hosts = relationship('Host')
    host_specs = relationship('DefaultSpec')
    nag_app_services = relationship(
        'NagApptypesServices',
        primaryjoin='NagApptypesServices.app_id == AppDefinition.id'
    )
    nag_host_services = relationship('NagHostsServices')

    package_definitions = relationship(
        'PackageDefinition',
        secondary=lambda: Base.metadata.tables['project_package'],
        passive_deletes=True,
        back_populates='applications',
    )

    projects = relationship(
        'Project',
        secondary=lambda: Base.metadata.tables['project_package'],
        passive_deletes=True,
        back_populates='applications',
    )
