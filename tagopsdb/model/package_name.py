from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER

from .meta import Base, Column, String


class PackageName(Base):
    __tablename__ = 'package_names'

    id = Column(u'pkg_name_id', INTEGER(), primary_key=True)
    name = Column(String(length=255), nullable=False)
    pkg_def_id = Column(
        INTEGER(),
        ForeignKey('package_definitions.pkg_def_id', ondelete='cascade'),
        nullable=False
    )

    package_definition = relationship(
        'PackageDefinition',
        back_populates='package_names'
    )

    __table_args__ = (
        UniqueConstraint(u'name', u'pkg_def_id', name='name_pkg_def_id'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8',},
    )
