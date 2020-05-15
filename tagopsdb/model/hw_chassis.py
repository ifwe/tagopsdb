# Copyright 2020 The Meet Group, Inc.
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

from sqlalchemy import Enum, UniqueConstraint
from sqlalchemy.dialects.mysql import BOOLEAN, INTEGER, FLOAT
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class HwChassis(Base):
    __tablename__ = 'hw_chassis'

    chassis_id = Column(u'chassis_id', INTEGER(), primary_key=True)
    vendor = Column(String(length=20))
    height = Column(u'height', INTEGER())
    width = Column(u'width', FLOAT())
    depth = Column(u'depth', FLOAT())
    model = Column(String(length=20))
    control = Column(Enum(u'digi', u'ipmi', u'libvirt', u'rlm', u'vmware'))
    virtual = Column(BOOLEAN(), nullable=False, server_default='0')
    __table_args__ = (
        UniqueConstraint(u'vendor', u'model'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
