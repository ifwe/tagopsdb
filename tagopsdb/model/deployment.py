from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func

from .meta import Base, Column, String


class Deployment(Base):
    __tablename__ = 'deployments'

    id = Column(u'DeploymentID', INTEGER(), primary_key=True)
    package_id = Column(
        INTEGER(),
        ForeignKey('packages.package_id', ondelete='cascade'),
        nullable=False
    )
    user = Column(String(length=32), nullable=False)
    dep_type = Column(Enum('deploy', 'rollback'), nullable=False)
    declared = Column(
        TIMESTAMP(),
        nullable=False,
        server_default=func.current_timestamp()
    )
    app_deployments = relationship('AppDeployment')
    host_deployments = relationship('HostDeployment')
