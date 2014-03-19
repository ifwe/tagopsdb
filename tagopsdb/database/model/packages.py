from sqlalchemy import (
    Column, Enum, UniqueConstraint, ForeignKey, TIMESTAMP, VARCHAR
)
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func

from .base import Base

from .package_definitions import PackageDefinitions


class Packages(Base):
    __tablename__ = 'packages'

    id = Column(u'package_id', INTEGER(), primary_key=True)
    pkg_def_id = Column(INTEGER(),
                        ForeignKey(PackageDefinitions.id, ondelete='cascade'),
                        nullable=False)
    pkg_name = Column(VARCHAR(length=255), nullable=False)
    version = Column(VARCHAR(length=63), nullable=False)
    revision = Column(VARCHAR(length=63), nullable=False)
    status = Column(Enum('completed', 'failed', 'pending', 'processing',
                         'removed'), nullable=False)
    created = Column(TIMESTAMP(), nullable=False,
                     default=func.current_timestamp(),
                     server_default=func.current_timestamp())
    creator = Column(VARCHAR(length=255), nullable=False)
    builder = Column(Enum(u'developer', u'hudson', u'jenkins'),
                     nullable=False, default='developer',
                     server_default='developer')
    project_type = Column(Enum(u'application', u'kafka-config', u'tagconfig'),
                          nullable=False, default='application',
                          server_default='application')

    deployments = relationship('Deployments')

    __table_args__ = (
        UniqueConstraint(u'pkg_name', u'version', u'revision', u'builder',
                         name=u'unique_package'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'},
    )

    def __init__(self, pkg_def_id, pkg_name, version, revision, status,
                 created, creator, builder, project_type):
        """ """

        self.pkg_def_id = pkg_def_id
        self.pkg_name = pkg_name
        self.version = version
        self.revision = revision
        self.status = status
        self.created = created
        self.creator = creator
        self.builder = builder
        self.project_type = project_type
