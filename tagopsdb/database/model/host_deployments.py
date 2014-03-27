from sqlalchemy import Column, Enum, ForeignKey, TIMESTAMP, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.sql.expression import func

from .base import Base


class HostDeployments(Base):
    __tablename__ = 'host_deployments'

    id = Column(u'HostDeploymentID', INTEGER(), primary_key=True)
    deployment_id = Column(
        u'DeploymentID',
        INTEGER(),
        ForeignKey('deployments.DeploymentID', ondelete='cascade'),
        nullable=False
    )
    host_id = Column(u'HostID', INTEGER(),
                     ForeignKey('hosts.HostID', ondelete='cascade'),
                     nullable=False)
    user = Column(VARCHAR(length=32), nullable=False)
    status = Column(Enum('inprogress', 'failed', 'ok'), nullable=False)
    realized = Column(TIMESTAMP(), nullable=False,
                      default=func.current_timestamp(),
                      server_default=func.current_timestamp())

    def __init__(self, deployment_id, host_id, user, status, realized):
        """ """

        self.deployment_id = deployment_id
        self.host_id = host_id
        self.user = user
        self.status = status
        self.realized = realized
