from sqlalchemy import ForeignKey, Table
from sqlalchemy.dialects.mysql import INTEGER

from .meta import Base, Column


nag_contact_groups_members = Table(
    u'nag_contact_groups_members',
    Base.metadata,
    Column(u'contact_id', INTEGER(),
           ForeignKey('nag_contacts.id', ondelete='cascade'),
           primary_key=True),
    Column(u'contact_group_id', INTEGER(),
           ForeignKey('nag_contact_groups.id', ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)
