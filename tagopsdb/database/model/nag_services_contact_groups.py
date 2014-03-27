from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base

from .nag_contact_groups import NagContactGroups
from .nag_services import NagServices


NagServicesContactGroups = nag_services_contact_groups = Table(
    u'nag_services_contact_groups',
    Base.metadata,
    Column(u'service_id', INTEGER(),
           ForeignKey(NagServices.id, ondelete='cascade'),
           primary_key=True),
    Column(u'contact_group_id', INTEGER(),
           ForeignKey(NagContactGroups.id, ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)
