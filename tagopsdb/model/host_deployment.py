from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP
from sqlalchemy.sql.expression import func

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
    host_id = Column(
        u'HostID',
        INTEGER(),
        ForeignKey('hosts.HostID', ondelete='cascade'),
        nullable=False
    )
    user = Column(String(length=32), nullable=False)
    status = Column(Enum('inprogress', 'failed', 'ok'), nullable=False)
    realized = Column(
        TIMESTAMP(),
        nullable=False,
        server_default=func.current_timestamp()
    )
