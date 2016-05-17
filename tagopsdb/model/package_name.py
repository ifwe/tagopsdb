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

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER

from .meta import Base, Column, String


class PackageName(Base):
    __tablename__ = 'package_names'

    id = Column(u'pkg_name_id', INTEGER(), primary_key=True)
    name = Column(String(length=255), nullable=False)
    pkg_def_id = Column(
        INTEGER(),
        ForeignKey('package_definitions.pkg_def_id', ondelete='cascade'),
        nullable=False
    )

    package_definition = relationship(
        'PackageDefinition',
        back_populates='package_names'
    )

    __table_args__ = (
        UniqueConstraint(u'name', u'pkg_def_id', name='name_pkg_def_id'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8',},
    )
