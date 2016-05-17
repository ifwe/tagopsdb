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

from sqlalchemy import ForeignKey, Table, UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER

from .meta import Base, Column


net_default_trunk = Table(
    u'net_default_trunks',
    Base.metadata,
    Column(u'net_default_id', INTEGER(unsigned=True),
           ForeignKey('net_default_maps.net_default_id', ondelete='cascade'),
           nullable=False),
    Column(u'vlan_id', INTEGER(),
           ForeignKey('vlans.VlanID', ondelete='cascade'),
           nullable=False),
    UniqueConstraint(u'net_default_id', u'vlan_id', name='trunk_key'),
    mysql_engine='InnoDB', mysql_charset='utf8',
)
