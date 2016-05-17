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

from sqlalchemy import ForeignKey, Table
from sqlalchemy.dialects.mysql import INTEGER

from .meta import Base, Column


nag_contact_groups_members = Table(
    u'nag_contact_groups_members',
    Base.metadata,
    Column(u'contact_id', INTEGER(),
           ForeignKey('nag_contacts.id', ondelete='cascade'),
           primary_key=True),
    Column(u'contact_group_id', INTEGER(),
           ForeignKey('nag_contact_groups.id', ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)
