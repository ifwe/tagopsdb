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
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class HostInterface(Base):
    __tablename__ = 'host_interfaces'

    id = Column(u'InterfaceID', INTEGER(), primary_key=True)
    host_id = Column(
        u'HostID',
        INTEGER(),
        ForeignKey('hosts.HostID', ondelete='cascade'),
        index=True
    )
    network_id = Column(
        u'NetworkID',
        INTEGER(),
        ForeignKey('networkDevice.NetworkID', ondelete='cascade'),
        index = True
    )
    interface_name = Column(u'interfaceName', String(length=10))
    interface_type = Column(
        Enum('ethernet', 'power', 'fc', 'mgmt'),
        nullable=False,
        server_default='ethernet',
    )
    mac_address = Column(u'macAddress', String(length=18), unique=True)
    port_id = Column(
        u'PortID',
        INTEGER(),
        ForeignKey('ports.PortID'),
        unique=True,
        index=True
    )
    host_ips = relationship('HostIp', backref='host_interface')

    __table_args__ = (
        UniqueConstraint(u'HostID', u'interfaceName'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
