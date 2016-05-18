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

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship

from .meta import Base, Column


class ProjectPackage(Base):
    __tablename__ = 'project_package'

    project_id = Column(
        INTEGER(),
        ForeignKey('projects.project_id', ondelete='cascade'),
        primary_key=True
    )
    pkg_def_id = Column(
        INTEGER(),
        ForeignKey('package_definitions.pkg_def_id', ondelete='cascade'),
        primary_key=True
    )
    app_id = Column(
        SMALLINT(display_width=6),
        ForeignKey('app_definitions.AppID', ondelete='cascade'),
        primary_key=True
    )

    app_definition = relationship('AppDefinition', uselist=False)
    package_definition = relationship('PackageDefinition', uselist=False)
    project = relationship('Project', uselist=False)
