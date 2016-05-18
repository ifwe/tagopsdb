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
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from .meta import Base, Column


class NsWeight(Base):
    __tablename__ = 'ns_weight'

    vip_id = Column(
        u'vipID',
        INTEGER(unsigned=True),
        ForeignKey('ns_vip.vipID', ondelete='cascade'),
        primary_key=True
    )
    spec_id = Column(
        u'specID',
        INTEGER(),
        ForeignKey('host_specs.specID', ondelete='cascade'),
        primary_key=True
    )
    weight = Column(TINYINT(display_width=3, unsigned=True), nullable=False)
    host_spec = relationship('NsVip', uselist=False, backref='ns_vip_assocs')
