from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship

from .meta import Base, Column


class ProjectPackage(Base):
    __tablename__ = 'project_package'

    project_id = Column(
        INTEGER(),
        ForeignKey('projects.project_id', ondelete='cascade'),
        primary_key=True
    )
    pkg_def_id = Column(
        INTEGER(),
        ForeignKey('package_definitions.pkg_def_id', ondelete='cascade'),
        primary_key=True
    )
    app_id = Column(
        SMALLINT(display_width=6),
        ForeignKey('app_definitions.AppID', ondelete='cascade'),
        primary_key=True
    )

    app_definitions = relationship('AppDefinition')
    package_definitions = relationship('PackageDefinition')
    projects = relationship('Project')
