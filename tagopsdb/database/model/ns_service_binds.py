from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base

from .ns_monitor import NsMonitor
from .ns_service import NsService


NsServiceBinds = ns_service_binds = Table(
    u'ns_service_binds',
    Base.metadata,
    Column(u'serviceID', INTEGER(unsigned=True),
           ForeignKey(NsService.id, ondelete='cascade'),
           primary_key=True),
    Column(u'monitorID', INTEGER(unsigned=True),
           ForeignKey(NsMonitor.id, ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)
