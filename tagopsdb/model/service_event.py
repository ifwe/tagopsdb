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
from sqlalchemy.dialects.mysql import INTEGER, TEXT, TIMESTAMP
from sqlalchemy.sql.expression import func

from .meta import Base, Column, String


class ServiceEvent(Base):
    __tablename__ = 'serviceEvent'

    id = Column(u'ServiceID', INTEGER(), primary_key=True)
    host_id = Column(
        u'HostID',
        INTEGER(),
        ForeignKey('hosts.HostID', ondelete='cascade')
    )
    service_status = Column(u'serviceStatus', String(length=100))
    comments = Column(TEXT())
    service_date = Column(
        u'serviceDate',
        TIMESTAMP(),
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        server_onupdate=func.current_timestamp()
    )
