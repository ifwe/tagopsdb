from sqlalchemy import Column, Enum, ForeignKey, TIMESTAMP, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func

from .base import Base

from .packages import Packages


class Deployments(Base):
    __tablename__ = 'deployments'

    id = Column(u'DeploymentID', INTEGER(), primary_key=True)
    package_id = Column(INTEGER(),
                        ForeignKey(Packages.id, ondelete='cascade'),
                        nullable=False)
    user = Column(VARCHAR(length=32), nullable=False)
    dep_type = Column(Enum('deploy', 'rollback'), nullable=False)
    declared = Column(TIMESTAMP(), nullable=False,
                      default=func.current_timestamp(),
                      server_default=func.current_timestamp())

    app_deployments = relationship('AppDeployments')
    host_deployments = relationship('HostDeployments')

    def __init__(self, package_id, user, dep_type, declared):
        """ """

        self.package_id = package_id
        self.user = user
        self.dep_type = dep_type
        self.declared = declared
