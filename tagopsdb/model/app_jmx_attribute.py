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
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from .meta import Base, Column


app_jmx_attribute = Table(
    u'app_jmx_attributes',
    Base.metadata,
    Column(u'AppID', SMALLINT(display_width=6),
           ForeignKey('app_definitions.AppID', ondelete='cascade'),
           primary_key=True),
    Column(u'jmx_attribute_id', INTEGER(),
           ForeignKey('jmx_attributes.jmx_attribute_id', ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)
