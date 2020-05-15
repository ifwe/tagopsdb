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
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMTEXT, SMALLINT
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class HostSpec(Base):
    __tablename__ = 'host_specs'

    id = Column(u'specID', INTEGER(), primary_key=True)
    chassis_id = Column(
        u'chassis_id', INTEGER(), ForeignKey('hw_chassis.chassis_id'),
    )
    gen = Column(String(length=4))
    memory_size = Column(u'memorySize', INTEGER(display_width=4))
    cores = Column(SMALLINT(display_width=2), nullable=False)
    cpu_speed = Column(u'cpuSpeed', INTEGER(display_width=6))
    disk_size = Column(u'diskSize', INTEGER(display_width=6))
    expansions = Column(MEDIUMTEXT())
    services = relationship('NsServiceMax')
    hw_chassis = relationship('HwChassis', uselist=False, backref='host_spec')
