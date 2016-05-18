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
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from .meta import Base, Column


class ApptypeAccess(Base):
    __tablename__ = 'apptype_access'
    
    environment_id = Column(
        INTEGER(),
        ForeignKey('environments.environmentID', ondelete='cascade'),
        primary_key=True
    )
    app_id = Column(
        SMALLINT(),
        ForeignKey('app_definitions.AppID', ondelete='cascade'),
        primary_key=True
    )
    gid = Column(
        INTEGER(unsigned=True),
        ForeignKey('ldap_groups.gid', ondelete='cascade'),
        primary_key=True
    )
