from sqlalchemy import Enum
from sqlalchemy.dialects.mysql import BOOLEAN, INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class PackageLocation(Base):
    __tablename__ = 'package_locations'

    id = Column(u'pkgLocationID', INTEGER(), primary_key=True)
    project_type = Column(
        Enum(u'application', u'kafka-config', u'tagconfig'),
        nullable=False,
        server_default='application'
    )
    pkg_type = Column(String(length=255), nullable=False)
    pkg_name = Column(String(length=255), nullable=False, unique=True)
    app_name = Column(String(length=255), nullable=False, unique=True)
    path = Column(String(length=255), nullable=False, unique=True)
    arch = Column(
        Enum(u'i386', u'x86_64', u'noarch'),
        nullable=False,
        server_default='noarch'
    )
    build_host = Column(String(length=30), nullable=False)
    environment = Column(BOOLEAN(), nullable=False)
    app_definitions = relationship(
        'AppDefinition',
        secondary='app_packages',
        backref='package_locations'
    )
