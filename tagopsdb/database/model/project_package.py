from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from sqlalchemy.orm import relationship

from .base import Base

from .app_definitions import AppDefinitions
from .package_definitions import PackageDefinitions
from .projects import Projects


class ProjectPackage(Base):
    __tablename__ = 'project_package'

    project_id = Column(INTEGER(),
                        ForeignKey(Projects.id, ondelete='cascade'),
                        primary_key=True)
    pkg_def_id = Column(INTEGER(),
                        ForeignKey(PackageDefinitions.id, ondelete='cascade'),
                        primary_key=True)
    app_id = Column(SMALLINT(display_width=6),
                    ForeignKey(AppDefinitions.id, ondelete='cascade'),
                    primary_key=True)

    app_definitions = relationship('AppDefinitions')
    package_definitions = relationship('PackageDefinitions')
    projects = relationship('Projects')
