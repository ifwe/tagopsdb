from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TIMESTAMP
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

    environment_obj = relationship('Environment')

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
