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


class Port(Base):
    __tablename__ = 'ports'

    id = Column(u'PortID', INTEGER(), primary_key=True)
    network_id = Column(
        u'NetworkID',
        INTEGER(),
        ForeignKey('networkDevice.NetworkID', ondelete='cascade')
    )
    port_number = Column(u'portNumber', String(length=20))

    network_interface = relationship('HostInterface', uselist=False)

    __table_args__ = (
        UniqueConstraint('NetworkID', 'portNumber',
                         name='NetworkID_portNumber'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
