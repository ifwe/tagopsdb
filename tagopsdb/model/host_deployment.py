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
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP, FLOAT, TEXT
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import relationship, synonym

from .meta import Base, Column, String


class HostDeployment(Base):
    __tablename__ = 'host_deployments'

    id = Column(u'HostDeploymentID', INTEGER(), primary_key=True)
    deployment_id = Column(
        u'DeploymentID',
        INTEGER(),
        ForeignKey('deployments.DeploymentID', ondelete='cascade'),
        nullable=False
    )
    deployment = relationship("Deployment", uselist=False)

    host_id = Column(
        u'HostID',
        INTEGER(),
        ForeignKey('hosts.HostID', ondelete='cascade'),
        nullable=False
    )
    host = relationship("Host", uselist=False)

    package_id = Column(
        INTEGER(),
        ForeignKey('packages.package_id', ondelete='cascade'),
        nullable=False
    )
    package = relationship(
        "Package",
        uselist=False,
        back_populates='host_deployments',
    )

    user = Column(String(length=32), nullable=False)
    status = Column(
        Enum(
            'failed',
            'inprogress',
            'ok',
            'pending',
        ),
        nullable=False
    )
    realized = Column(
        TIMESTAMP(),
        nullable=False,
        server_default=func.current_timestamp()
    )
    created_at = synonym('realized')
    duration = Column(FLOAT(), nullable=False, server_default="0")
    deploy_result = Column(TEXT())
