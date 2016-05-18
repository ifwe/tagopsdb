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


class Environment(Base):
    __tablename__ = 'environments'

    id = Column(u'environmentID', INTEGER(), primary_key=True)
    environment = Column(String(length=15), nullable=False, unique=True)
    env = Column(String(length=12), nullable=False, unique=True)
    domain = Column(String(length=32), nullable=False, unique=True)
    prefix = Column(String(length=1), nullable=False)
    zone_id = Column(INTEGER(), ForeignKey('zones.ZoneID'), nullable=False)
    zone = relationship('Zone', uselist=False)
