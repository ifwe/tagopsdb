from sqlalchemy import Column, Enum, ForeignKey, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from sqlalchemy.orm import relationship

from .base import Base

from .ganglia import Ganglia
from .vlans import Vlans


class AppDefinitions(Base):
    __tablename__ = 'app_definitions'

    id = Column(u'AppID', SMALLINT(display_width=2), primary_key=True)
    production_vlan_id = Column(u'Production_VlanID', INTEGER(),
                                ForeignKey(Vlans.id), nullable=False)
    development_vlan_id = Column(u'Development_VlanID', INTEGER(),
                                 ForeignKey(Vlans.id), nullable=False)
    staging_vlan_id = Column(u'Staging_VlanID', INTEGER(),
                             ForeignKey(Vlans.id), nullable=False)
    distribution = Column(Enum(u'co54', u'co62', u'co64', u'co65', u'rh53',
                               u'rh62', u'rh63', u'rh64'), nullable=False,
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

    app_deployments = relationship('AppDeployments')
    hipchats = relationship(
        'Hipchat',
        secondary='app_hipchat_rooms',
        backref='app_definitions'
    )
    hosts = relationship('Hosts')
    host_specs = relationship('DefaultSpecs')
    ns_services = relationship('NsVipBinds')
    nag_app_services = relationship(
        'NagApptypesServices',
        primaryjoin='NagApptypesServices.app_id == AppDefinitions.id'
    )
    nag_host_services = relationship('NagHostsServices')
    proj_pkg = relationship('ProjectPackage')
    development_vlans = relationship(
        'Vlans',
        foreign_keys=[development_vlan_id]
    )
    production_vlans = relationship('Vlans', foreign_keys=[production_vlan_id])
    staging_vlans = relationship('Vlans', foreign_keys=[staging_vlan_id])

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
