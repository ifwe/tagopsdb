from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP
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
