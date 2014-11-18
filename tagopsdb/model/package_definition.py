from sqlalchemy import Enum
from sqlalchemy.dialects.mysql import BOOLEAN, INTEGER, TIMESTAMP
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.sql import and_
from sqlalchemy.sql.expression import func

from .meta import Base, Column, HasDummy, String


class PackageDefinition(Base, HasDummy):
    __tablename__ = 'package_definitions'

    id = Column(u'pkg_def_id', INTEGER(), primary_key=True)
    deploy_type = Column(String(length=30), nullable=False)
    validation_type = Column(String(length=15), nullable=False)
    pkg_name = Column(String(length=255), nullable=False)
    name = synonym('pkg_name')
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
    environment_specific = synonym('env_specific')

    created = Column(
        TIMESTAMP(),
        nullable=False,
        server_default=func.current_timestamp()
    )

    packages = relationship(
        'Package',
        primaryjoin=(
            "(Package.pkg_def_id == PackageDefinition.id)"
            " & (Package.status != 'removed')"
        ),
        passive_deletes=True,
    )

    all_packages = relationship(
        'Package',
        back_populates='package_definition',
        passive_deletes=True,
    )

    package_names = relationship(
        'PackageName',
        back_populates="package_definition",
        passive_deletes=True,
    )

    applications = relationship(
        'AppDefinition',
        secondary=lambda: Base.metadata.tables['project_package'],
        passive_deletes=True,
        back_populates='package_definitions',
        viewonly=True,
    )

    projects = relationship(
        'Project',
        secondary=lambda: Base.metadata.tables['project_package'],
        passive_deletes=True,
        back_populates='package_definitions',
        viewonly=True,
    )
