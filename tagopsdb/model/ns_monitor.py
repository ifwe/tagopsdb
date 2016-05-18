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

from sqlalchemy.dialects.mysql import INTEGER

from .meta import Base, Column, String


class NsMonitor(Base):
    __tablename__ = 'ns_monitor'

    id = Column(u'monitorID', INTEGER(unsigned=True), primary_key=True)
    monitor = Column(String(length=32), nullable=False, unique=True)
