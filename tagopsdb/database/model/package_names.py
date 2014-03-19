from sqlalchemy import Column, UniqueConstraint, ForeignKey, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base

from .package_definitions import PackageDefinitions


class PackageNames(Base):
    __tablename__ = 'package_names'

    id = Column(u'pkg_name_id', INTEGER(), primary_key=True)
    name = Column(VARCHAR(length=255), nullable=False)
    pkg_def_id = Column(INTEGER(),
                        ForeignKey(PackageDefinitions.id, ondelete='cascade'),
                        nullable=False)

    __table_args__ = (
        UniqueConstraint(u'name', u'pkg_def_id', name='name_pkg_def_id'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'},
    )

    def __init__(self, name, pkg_def_id=None):
        """ """

        self.name = name
        self.pkg_def_id = pkg_def_id
