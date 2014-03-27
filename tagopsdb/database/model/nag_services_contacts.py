from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base

from .nag_contacts import NagContacts
from .nag_services import NagServices


NagServicesContacts = nag_services_contacts = Table(
    u'nag_services_contacts',
    Base.metadata,
    Column(u'service_id', INTEGER(),
           ForeignKey(NagServices.id, ondelete='cascade'),
           primary_key=True),
    Column(u'contact_id', INTEGER(),
           ForeignKey(NagContacts.id, ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)
