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


class Datacenter(Base):
    __tablename__ = 'datacenters'

    id = Column(u'dc_id', INTEGER(), primary_key=True)

    dc_name = Column(String(length=32), unique=True, nullable=False)
    physical_location = Column(String(length=64), nullable=False)
    priority = Column(INTEGER(), nullable=False)
