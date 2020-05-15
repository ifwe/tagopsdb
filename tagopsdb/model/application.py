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

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship, synonym

from .meta import Base, Column, HasDummy, String


class AppDefinition(Base, HasDummy):
    __tablename__ = 'app_definitions'

    id = Column(u'AppID', SMALLINT(display_width=2), primary_key=True)
    distribution = Column(String(length=20), nullable=False)
    app_type = Column(u'appType', String(length=100), nullable=False)
    name = synonym('app_type')
    host_base = Column(u'hostBase', String(length=100))
    puppet_class = Column(
        u'puppetClass',
        String(length=100),
        nullable=False,
        server_default='baseclass',
    )
    ganglia_id = Column(
        u'GangliaID',
        INTEGER(),
        ForeignKey('ganglia.GangliaID'),
        nullable=False,
        server_default='1',
    )
    description = Column(String(length=100))
    doc_url = Column(String(length=512))
    status = Column(
        Enum('active', 'inactive'),
        nullable=False,
        server_default='active',
    )

    app_deployments = relationship(
        'AppDeployment',
        order_by='desc(AppDeployment.created_at), AppDeployment.id',
        lazy='dynamic',
    )
    hipchats = relationship(
        'Hipchat',
        secondary='app_hipchat_rooms',
        back_populates='app_definitions',
    )
    hosts = relationship('Host')
    host_specs = relationship('DefaultSpec')
    nag_app_services = relationship(
        'NagApptypesServices',
        primaryjoin='NagApptypesServices.app_id == AppDefinition.id',
    )
    nag_host_services = relationship('NagHostsServices')

    package_definitions = relationship(
        'PackageDefinition',
        secondary=lambda: Base.metadata.tables['project_package'],
        passive_deletes=True,
        back_populates='applications',
        viewonly=True,
    )

    projects = relationship(
        'Project',
        secondary=lambda: Base.metadata.tables['project_package'],
        passive_deletes=True,
        back_populates='applications',
        viewonly=True,
    )
