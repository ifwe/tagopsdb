from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TIMESTAMP
from sqlalchemy.sql.expression import func

from .meta import Base, Column, String


class AppDeployment(Base):
    __tablename__ = 'app_deployments'

    id = Column(u'AppDeploymentID', INTEGER(), primary_key=True)
    deployment_id = Column(
        u'DeploymentID',
        INTEGER(),
        ForeignKey('deployments.DeploymentID', ondelete='cascade'),
        nullable=False
    )
    app_id = Column(
        u'AppID',
        SMALLINT(display_width=6),
        ForeignKey('app_definitions.AppID', ondelete='cascade'),
        nullable=False
    )
    user = Column(String(length=32), nullable=False)
    status = Column(
        Enum(
            'complete',
            'incomplete',
            'inprogress',
            'invalidated',
            'validated',
        ),
        nullable=False
    )
    environment = Column(String(length=15), nullable=False)
    realized = Column(
        TIMESTAMP(),
        nullable=False,
        server_default=func.current_timestamp()
    )
