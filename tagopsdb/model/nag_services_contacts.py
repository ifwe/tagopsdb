from sqlalchemy import ForeignKey, Table
from sqlalchemy.dialects.mysql import INTEGER

from .meta import Base, Column


nag_services_contacts = Table(
    u'nag_services_contacts',
    Base.metadata,
    Column(u'service_id', INTEGER(),
           ForeignKey('nag_services.id', ondelete='cascade'),
           primary_key=True),
    Column(u'contact_id', INTEGER(),
           ForeignKey('nag_contacts.id', ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)
