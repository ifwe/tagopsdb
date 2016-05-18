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
from sqlalchemy.dialects.mysql import DATE, INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Asset(Base):
    __tablename__ = 'asset'

    id = Column(u'AssetID', INTEGER(), primary_key=True)
    host_id = Column(
        u'HostID',
        INTEGER(),
        ForeignKey('hosts.HostID', ondelete='cascade'),
        nullable=False
    )
    oem_serial = Column(u'oemSerial', String(length=30), unique=True)
    service_tag = Column(u'serviceTag', String(length=20))
    tagged_serial = Column(u'taggedSerial', String(length=20))

    host = relationship('Host', uselist=False)
