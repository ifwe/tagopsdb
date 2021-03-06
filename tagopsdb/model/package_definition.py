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
from sqlalchemy.dialects.mysql import BOOLEAN, INTEGER, TIMESTAMP
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.sql import and_
from sqlalchemy.sql.expression import func

from .meta import Base, Column, HasDummy, String


class PackageDefinition(Base, HasDummy):
    __tablename__ = 'package_definitions'

    id = Column(u'pkg_def_id', INTEGER(), primary_key=True)
    deploy_type = Column(String(length=30), nullable=False)
    validation_type = Column(String(length=15), nullable=False)
    pkg_name = Column(String(length=255), nullable=False)
    name = synonym('pkg_name')
    path = Column(String(length=255), nullable=False)
    repository = Column(String(length=255), nullable=True)
    arch = Column(
        Enum('i386', 'x86_64', 'noarch'),
        nullable=False,
        server_default='noarch'
    )
    build_type = Column(
        Enum(u'developer', u'hudson', u'jenkins'),
        nullable=False,
        server_default='jenkins'
    )
    build_host = Column(String(length=255), nullable=False)
    env_specific = Column(BOOLEAN(), nullable=False, server_default='0')
    environment_specific = synonym('env_specific')

    created = Column(
        TIMESTAMP(),
        nullable=False,
        server_default=func.current_timestamp()
    )

    packages = relationship(
        'Package',
        primaryjoin=(
            "(Package.pkg_def_id == PackageDefinition.id)"
            " & (Package.status != 'removed')"
        ),
        passive_deletes=True,
    )

    all_packages = relationship(
        'Package',
        back_populates='package_definition',
        passive_deletes=True,
    )

    package_names = relationship(
        'PackageName',
        back_populates="package_definition",
        passive_deletes=True,
    )

    applications = relationship(
        'AppDefinition',
        secondary=lambda: Base.metadata.tables['project_package'],
        passive_deletes=True,
        back_populates='package_definitions',
        viewonly=True,
    )

    projects = relationship(
        'Project',
        secondary=lambda: Base.metadata.tables['project_package'],
        passive_deletes=True,
        back_populates='package_definitions',
        viewonly=True,
    )
