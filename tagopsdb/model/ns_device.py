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

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class NsDevice(Base):
    __tablename__ = 'ns_device'

    id = Column(u'deviceID', INTEGER(unsigned=True), primary_key=True)
    proto = Column(String(length=6), nullable=False)
    host = Column(String(length=32), nullable=False)
    vips = relationship('NsVip')

    __table_args__ = (
        UniqueConstraint(u'proto', u'host', name=u'proto_host'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
