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


class Vlan(Base):
    __tablename__ = 'vlans'

    id = Column(u'VlanID', INTEGER(), primary_key=True)
    name = Column(
        String(length=20),
        nullable=False,
        unique=True
    )
    environment_id = Column(
        u'environmentID',
        INTEGER(),
        ForeignKey('environments.environmentID', ondelete='cascade')
    )
    description = Column(String(length=50))
    subnets = relationship('Subnet')
