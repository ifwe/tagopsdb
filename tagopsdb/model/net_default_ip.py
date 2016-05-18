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

from .meta import Base, Column


class NetDefaultIP(Base):
    __tablename__ = 'net_default_ips'

    id = Column(
        u'net_default_ip_id',
        INTEGER(unsigned=True),
        primary_key=True
    )
    net_default_id = Column(
        INTEGER(unsigned=True),
        ForeignKey('net_default_maps.net_default_id', ondelete='cascade'),
        nullable=False
    )
    vlan_id = Column(
        INTEGER(),
        ForeignKey('vlans.VlanID', ondelete='cascade'),
        nullable=False
    )
    priority = Column(INTEGER(unsigned=True), nullable=False)
    ns_services = relationship('NsVipBinds')
    ns_vips = relationship('NsVipBinds')

    __table_args__ = (
        UniqueConstraint(
            u'net_default_id',
            u'vlan_id',
            u'priority',
            name='ip_key'
        ),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
