from sqlalchemy import Column, Enum, TIMESTAMP, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN

from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func

from .base import Base


class PackageDefinitions(Base):
    __tablename__ = 'package_definitions'

    id = Column(u'pkg_def_id', INTEGER(), primary_key=True)
    deploy_type = Column(VARCHAR(length=30), nullable=False)
    validation_type = Column(VARCHAR(length=15), nullable=False)
    pkg_name = Column(VARCHAR(length=255), nullable=False)
    path = Column(VARCHAR(length=255), nullable=False)
    arch = Column(Enum('i386', 'x86_64', 'noarch'), nullable=False,
                  default='noarch', server_default='noarch')
    build_type = Column(Enum(u'developer', u'hudson', u'jenkins'),
                        nullable=False, default='jenkins',
                        server_default='jenkins')
    build_host = Column(VARCHAR(length=255), nullable=False)
    env_specific = Column(BOOLEAN(), nullable=False, default=0,
                          server_default='0')
    created = Column(TIMESTAMP(), nullable=False,
                     default=func.current_timestamp(),
                     server_default=func.current_timestamp())

    packages = relationship('Packages', backref='package_definition')
    package_names = relationship('PackageNames')
    proj_pkg = relationship('ProjectPackage')

    def __init__(self, deploy_type, validation_type, pkg_name, path, arch,
                 build_type, build_host, env_specific, created):
        """ """

        self.deploy_type = deploy_type
        self.validation_type = validation_type
        self.pkg_name = pkg_name
        self.path = path
        self.arch = arch
        self.build_type = build_type
        self.build_host = build_host
        self.env_specific = env_specific
        self.created = created
