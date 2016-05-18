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


class Subnet(Base):
    __tablename__ = 'subnet'

    id = Column(u'SubnetID', INTEGER(), primary_key=True)
    vlan_id = Column(
        u'VlanID',
        INTEGER(),
        ForeignKey('vlans.VlanID', ondelete='cascade')
    )
    ip_address = Column(u'ipAddress', String(length=15), unique=True)
    netmask = Column(String(length=15))
    gateway = Column(String(length=15))
    zone_id = Column(u'ZoneID', INTEGER(), ForeignKey('zones.ZoneID'))
    zone = relationship('Zone', uselist=False, backref='subnets')
