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
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from .meta import Base, Column, String


class NetDefaultMap(Base):
    __tablename__ = 'net_default_maps'

    id = Column(u'net_default_id', INTEGER(unsigned=True), primary_key=True)
    dc_id = Column(
        INTEGER(),
        ForeignKey('datacenters.dc_id', ondelete='cascade'),
        server_default='1'
    )
    environment_id = Column(
        INTEGER(),
        ForeignKey('environments.environmentID', ondelete='cascade'),
        nullable=False
    )
    app_id = Column(
        SMALLINT(),
        ForeignKey('app_definitions.AppID', ondelete='cascade'),
        nullable=False
    )
    interface_name = Column(String(length=10), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            u'environment_id',
            u'app_id',
            u'interface_name',
            name='map_key'
        ),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
