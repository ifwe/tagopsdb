from sqlalchemy import Column, Enum, ForeignKey, TIMESTAMP, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func

from .base import Base


class AppDeployments(Base):
    __tablename__ = 'app_deployments'

    id = Column(u'AppDeploymentID', INTEGER(), primary_key=True)
    deployment_id = Column(
        u'DeploymentID',
        INTEGER(),
        ForeignKey('deployments.DeploymentID', ondelete='cascade'),
        nullable=False
    )
    app_id = Column(u'AppID', SMALLINT(display_width=6),
                    ForeignKey('app_definitions.AppID', ondelete='cascade'),
                    nullable=False)
    user = Column(VARCHAR(length=32), nullable=False)
    status = Column(Enum('complete', 'incomplete', 'inprogress',
                         'invalidated', 'validated'),
                    nullable=False)
    environment = Column(VARCHAR(length=15), nullable=False)
    realized = Column(TIMESTAMP(), nullable=False,
                      default=func.current_timestamp(),
                      server_default=func.current_timestamp())

    app = relationship('AppDefinitions', uselist=False)
    deployment = relationship('Deployments', uselist=False)

    def __init__(self, deployment_id, app_id, user, status, environment,
                 realized):
        """ """

        self.deployment_id = deployment_id
        self.app_id = app_id
        self.user = user
        self.status = status
        self.environment = environment
        self.realized = realized
