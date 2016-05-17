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
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Cname(Base):
    __tablename__ = 'cname'

    id = Column(u'CnameID', INTEGER(), primary_key=True)
    name = Column(String(length=40))
    ip_id = Column(
        u'IpID',
        INTEGER(),
        ForeignKey('host_ips.IpID', onupdate='cascade',
        ondelete='cascade')
    )
    zone_id = Column(
        u'ZoneID',
        INTEGER(),
        ForeignKey('zones.ZoneID', onupdate='cascade', ondelete='cascade')
    )
    host = relationship('HostIp', uselist=False)

    __table_args__ = (
        UniqueConstraint(u'name', u'ZoneID', name=u'name_ZoneID'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
