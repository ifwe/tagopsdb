from sqlalchemy import Enum
from sqlalchemy.dialects.mysql import BOOLEAN, INTEGER, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func

from .meta import Base, Column, String


class PackageDefinition(Base):
    __tablename__ = 'package_definitions'

    id = Column(u'pkg_def_id', INTEGER(), primary_key=True)
    deploy_type = Column(String(length=30), nullable=False)
    validation_type = Column(String(length=15), nullable=False)
    pkg_name = Column(String(length=255), nullable=False)
    path = Column(String(length=255), nullable=False)
    arch = Column(
        Enum('i386', 'x86_64', 'noarch'),
        nullable=False,
        server_default='noarch'
    )
    build_type = Column(
        Enum(u'developer', u'hudson', u'jenkins'),
        nullable=False,
        server_default='jenkins'
    )
    build_host = Column(String(length=255), nullable=False)
    env_specific = Column(BOOLEAN(), nullable=False, server_default='0')
    created = Column(
        TIMESTAMP(),
        nullable=False,
        server_default=func.current_timestamp()
    )
    packages = relationship('Package', backref='package_definition')
    package_names = relationship('PackageName')
    proj_pkg = relationship('ProjectPackage')
