from sqlalchemy import ForeignKey, Table
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from .meta import Base, Column


app_jmx_attribute = Table(
    u'app_jmx_attributes',
    Base.metadata,
    Column(u'AppID', SMALLINT(display_width=6),
           ForeignKey('app_definitions.AppID', ondelete='cascade'),
           primary_key=True),
    Column(u'jmx_attribute_id', INTEGER(),
           ForeignKey('jmx_attributes.jmx_attribute_id', ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)
