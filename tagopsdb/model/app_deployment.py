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

from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import BOOLEAN, INTEGER, SMALLINT, TIMESTAMP, FLOAT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.sql.expression import func, select

from .meta import Base, Column, String
from .environment import Environment


class AppDeployment(Base):
    __tablename__ = 'app_deployments'

    id = Column(u'AppDeploymentID', INTEGER(), primary_key=True)
    deployment_id = Column(
        u'DeploymentID',
        INTEGER(),
        ForeignKey('deployments.DeploymentID', ondelete='cascade'),
        nullable=False
    )
    deployment = relationship("Deployment", uselist=False)

    app_id = Column(
        u'AppID',
        SMALLINT(display_width=6),
        ForeignKey('app_definitions.AppID', ondelete='cascade'),
        nullable=False
    )
    application = relationship("AppDefinition", uselist=False)
    target = synonym('application')

    package_id = Column(
        INTEGER(),
        ForeignKey('packages.package_id', ondelete='cascade'),
        nullable=False
    )
    package = relationship(
        "Package",
        uselist=False,
        back_populates="app_deployments",
    )

    user = Column(String(length=32), nullable=False)
    status = Column(
        Enum(
            'complete',
            'incomplete',
            'inprogress',
            'invalidated',
            'pending',
            'validated',
        ),
        nullable=False
    )
    environment_id = Column(
        u'environment_id',
        INTEGER(),
        ForeignKey('environments.environmentID', ondelete='cascade'),
        nullable=False
    )
    realized = Column(
        TIMESTAMP(),
        nullable=False,
        server_default=func.current_timestamp()
    )
    created_at = synonym('realized')
    duration = Column(FLOAT(), nullable=False, server_default="0")
    skewed = Column(BOOLEAN(), nullable=False, server_default='0')

    environment_obj = relationship('Environment')

    __table_args__ = (
        UniqueConstraint(
            u'package_id', u'AppID', u'environment_id', u'realized'
        ),
    )

    @hybrid_property
    def env(self):
        return self.environment_obj.env

    @env.expression
    def env(cls):
        return select([Environment.env]).\
            where(Environment.id == cls.environment_id).correlate(cls).\
            label('env')

    @hybrid_property
    def environment(self):
        return self.environment_obj.environment

    @environment.expression
    def environment(cls):
        return select([Environment.environment]).\
            where(Environment.id == cls.environment_id).correlate(cls).\
            label('environment')

    @hybrid_property
    def needs_validation(self):
        """
        Complete and incomplete deployments require validation
        """
        return self.status in ('complete', 'incomplete')

    @needs_validation.expression
    def needs_validation(cls):
        return cls.status.in_(['complete', 'incomplete'])
