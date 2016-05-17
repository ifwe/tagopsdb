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

from sqlalchemy import Enum
from sqlalchemy.dialects.mysql import BOOLEAN, INTEGER
from sqlalchemy.orm import relationship, synonym

from .meta import Base, Column, String


class PackageLocation(Base):
    __tablename__ = 'package_locations'

    id = Column(u'pkgLocationID', INTEGER(), primary_key=True)
    project_type = Column(
        Enum(u'application', u'kafka-config', u'tagconfig'),
        nullable=False,
        server_default='application'
    )
    pkg_type = Column(String(length=255), nullable=False)
    pkg_name = Column(String(length=255), nullable=False, unique=True)
    name = synonym('pkg_name')
    app_name = Column(String(length=255), nullable=False, unique=True)
    path = Column(String(length=255), nullable=False, unique=True)
    arch = Column(
        Enum(u'i386', u'x86_64', u'noarch'),
        nullable=False,
        server_default='noarch'
    )
    build_host = Column(String(length=30), nullable=False)
    environment = Column(BOOLEAN(), nullable=False)
    app_definitions = relationship(
        'AppDefinition',
        secondary='app_packages',
        backref='package_locations'
    )
