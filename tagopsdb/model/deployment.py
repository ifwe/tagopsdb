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

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP, FLOAT
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.sql.expression import func

from .meta import Base, Column, String


class Deployment(Base):
    __tablename__ = 'deployments'

    id = Column(u'DeploymentID', INTEGER(), primary_key=True)

    user = Column(String(length=32), nullable=False)
    status = Column(
        Enum('pending', 'queued', 'inprogress', 'complete', 'failed',
             'canceled', 'stopped'),
        server_default='pending',
        nullable=False,
    )
    delay = Column(u'delay', INTEGER(), server_default='0')
    declared = Column(
        TIMESTAMP(),
        nullable=False,
        server_default=func.current_timestamp()
    )
    created_at = synonym('declared')
    duration = Column(FLOAT(), nullable=False, server_default="0")
    app_deployments = relationship(
        'AppDeployment', order_by="AppDeployment.created_at, AppDeployment.id"
    )
    host_deployments = relationship(
        'HostDeployment', order_by="HostDeployment.created_at, HostDeployment.id"
    )
