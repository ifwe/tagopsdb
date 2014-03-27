from sqlalchemy import Column, Enum, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN

from sqlalchemy.orm import relationship

from .base import Base

from .app_packages import AppPackages


class PackageLocations(Base):
    __tablename__ = 'package_locations'

    id = Column(u'pkgLocationID', INTEGER(), primary_key=True)
    project_type = Column(Enum(u'application', u'kafka-config', u'tagconfig'),
                          nullable=False, default='application',
                          server_default='application')
    pkg_type = Column(VARCHAR(length=255), nullable=False)
    pkg_name = Column(VARCHAR(length=255), nullable=False, unique=True)
    app_name = Column(VARCHAR(length=255), nullable=False, unique=True)
    path = Column(VARCHAR(length=255), nullable=False, unique=True)
    arch = Column(Enum(u'i386', u'x86_64', u'noarch'), nullable=False,
                  default='noarch', server_default='noarch')
    build_host = Column(VARCHAR(length=30), nullable=False)
    environment = Column(BOOLEAN(), nullable=False)

    app_definitions = relationship(
        'AppDefinitions',
        secondary=AppPackages,
        backref='package_locations'
    )

    def __init__(self, project_type, pkg_type, pkg_name, app_name, path, arch,
                 build_host, environment=False):
        """ """

        self.project_type = project_type
        self.pkg_type = pkg_type
        self.pkg_name = pkg_name
        self.app_name = app_name
        self.path = path
        self.arch = arch
        self.build_host = build_host
        self.environment = environment
