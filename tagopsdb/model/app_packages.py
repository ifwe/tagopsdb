from sqlalchemy import ForeignKey, Table
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from .meta import Base, Column


app_package = Table(
    u'app_packages',
    Base.metadata,
    Column(u'pkgLocationID', INTEGER(),
           ForeignKey('package_locations.pkgLocationID', ondelete='cascade'),
           primary_key=True),
    Column(u'AppID', SMALLINT(display_width=6),
           ForeignKey('app_definitions.AppID', ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)
