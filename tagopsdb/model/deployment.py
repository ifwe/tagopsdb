from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP
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
    app_deployments = relationship(
        'AppDeployment', order_by="AppDeployment.created_at, AppDeployment.id"
    )
    host_deployments = relationship(
        'HostDeployment', order_by="HostDeployment.created_at, HostDeployment.id"
    )
