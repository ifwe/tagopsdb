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
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class HostIp(Base):
    __tablename__ = 'host_ips'

    id = Column(u'IpID', INTEGER(), primary_key=True)
    interface_id = Column(
        u'InterfaceID',
        INTEGER(),
        ForeignKey('host_interfaces.InterfaceID', ondelete='cascade'),
        nullable=False,
        index=True
    )
    subnet_id = Column(
        u'SubnetID',
        INTEGER(),
        ForeignKey('subnet.SubnetID', ondelete='cascade'),
        nullable=False,
        unique=True,
        index=True
    )
    priority = Column(
        INTEGER(unsigned=True),
        nullable=False,
        server_default='1'
    )
    a_record = Column(u'ARecord', String(length=200))
    comments = Column(String(length=200))
    subnet = relationship('Subnet', uselist=False, backref='host_ip')
