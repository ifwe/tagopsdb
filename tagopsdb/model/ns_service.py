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

from sqlalchemy.dialects.mysql import SMALLINT, INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class NsService(Base):
    __tablename__ = 'ns_service'

    id = Column(u'serviceID', INTEGER(unsigned=True), primary_key=True)
    service_name = Column(
        u'serviceName',
        String(length=64),
        nullable=False,
        unique=True
    )
    proto = Column(String(length=16), nullable=False)
    port = Column(SMALLINT(display_width=5, unsigned=True), nullable=False)
    ns_monitors = relationship('NsMonitor', secondary='ns_service_binds')
    service_params = relationship('NsServiceParam')
