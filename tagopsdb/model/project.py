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

from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Project(Base):
    __tablename__ = 'projects'

    id = Column(u'project_id', INTEGER(), primary_key=True)
    name = Column(String(length=255), nullable=False, unique=True)

    applications = relationship(
        'AppDefinition',
        secondary=lambda: Base.metadata.tables['project_package'],
        passive_deletes=True,
        lazy=False,
        back_populates='projects',
        viewonly=True,
    )

    package_definitions = relationship(
        'PackageDefinition',
        secondary=lambda: Base.metadata.tables['project_package'],
        passive_deletes=True,
        back_populates='projects',
        viewonly=True,
    )

    @property
    def targets(self):
        return self.applications
