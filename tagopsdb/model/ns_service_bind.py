from sqlalchemy import ForeignKey, Table
from sqlalchemy.dialects.mysql import INTEGER

from .meta import Base, Column


ns_service_bind = Table(
    u'ns_service_binds',
    Base.metadata,
    Column(u'serviceID', INTEGER(unsigned=True),
           ForeignKey('ns_service.serviceID', ondelete='cascade'),
           primary_key=True),
    Column(u'monitorID', INTEGER(unsigned=True),
           ForeignKey('ns_monitor.monitorID', ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)
