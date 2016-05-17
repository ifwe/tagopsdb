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
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.sql.expression import func

from .meta import Base, Column, String


class Package(Base):
    __tablename__ = 'packages'

    id = Column(u'package_id', INTEGER(), primary_key=True)
    pkg_def_id = Column(
        INTEGER(),
        ForeignKey('package_definitions.pkg_def_id', ondelete='cascade'),
        nullable=False
    )
    pkg_name = Column(String(length=255), nullable=False)
    name = synonym('pkg_name')
    version = Column(String(length=63), nullable=False)
    revision = Column(String(length=63), nullable=False)
    job = Column(String(length=255), nullable=True)
    commit_hash = Column(String(length=40), nullable=True)
    status = Column(
        Enum('completed', 'failed', 'pending', 'processing', 'removed'),
        nullable=False
    )
    created = Column(
        TIMESTAMP(),
        nullable=False,
        server_default=func.current_timestamp()
    )
    creator = Column(String(length=255), nullable=False)
    builder = Column(
        Enum(u'developer', u'hudson', u'jenkins'),
        nullable=False,
        server_default='developer'
    )
    project_type = Column(
        Enum(u'application', u'kafka-config', u'tagconfig'),
        nullable=False,
        server_default='application'
    )
    package_definition = relationship(
        'PackageDefinition',
        back_populates='packages'
    )
    application = synonym('package_definition')
    app_deployments = relationship(
        'AppDeployment',
        back_populates='package',
        order_by="AppDeployment.created_at, AppDeployment.id"
    )
    host_deployments = relationship(
        'HostDeployment',
        back_populates='package',
        order_by="HostDeployment.created_at, HostDeployment.id"
    )

    __table_args__ = (
        UniqueConstraint(u'pkg_name', u'version', u'revision', u'builder',
                         name=u'unique_package'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
