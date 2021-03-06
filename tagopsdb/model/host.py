# Copyright 2016 Ifwe Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.sql.expression import select

from .meta import Base, Column, String
from .environment import Environment


class Host(Base):
    __tablename__ = 'hosts'

    id = Column(u'HostID', INTEGER(), primary_key=True)
    spec_id = Column(u'SpecID', INTEGER(), ForeignKey('host_specs.specID'))
    state = Column(
        Enum(
            u'baremetal',
            u'operational',
            u'repair',
            u'parts',
            u'reserved',
            u'escrow'
        ),
        nullable=False
    )
    hostname = Column(String(length=30))
    name = synonym('hostname')
    distribution = Column(String(length=20))
    app_id = Column(
        u'AppID',
        SMALLINT(display_width=6),
        ForeignKey('app_definitions.AppID'),
        server_default=None
    )
    dc_id = Column(
        INTEGER(),
        ForeignKey('datacenters.dc_id', ondelete='cascade'),
        server_default='1'
    )
    cage_location = Column(u'cageLocation', INTEGER())
    cab_location = Column(u'cabLocation', String(length=10))
    elevation = Column(u'elevation', INTEGER())
    environment_id = Column(
        u'environment_id',
        INTEGER(),
        ForeignKey('environments.environmentID', ondelete='cascade'),
        server_default=None
    )

    environment_obj = relationship('Environment')
    host_deployments = relationship('HostDeployment')
    host_interfaces = relationship('HostInterface', backref='host')
    host_spec = relationship('HostSpec', uselist=False, backref='hosts')
    ilom = relationship('Ilom', uselist=False, backref='host')
    service_events = relationship('ServiceEvent', backref='host')
    vm = relationship('VmInfo', uselist=False, back_populates='host')
    application = relationship('AppDefinition', uselist=False)
    target = synonym('application')
    datacenter = relationship('Datacenter', uselist=False)

    @hybrid_property
    def environment(self):
        return getattr(self.environment_obj, 'environment', None)

    @environment.expression
    def environment(cls):
        return select([Environment.environment]).\
                where(Environment.id == cls.environment_id).correlate(cls).\
                label('environment')

    __table_args__ = (
        UniqueConstraint(u'cageLocation', u'cabLocation', u'elevation'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
