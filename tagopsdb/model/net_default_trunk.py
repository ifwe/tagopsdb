from sqlalchemy import ForeignKey, Table, UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER

from .meta import Base, Column


net_default_trunk = Table(
    u'net_default_trunks',
    Base.metadata,
    Column(u'net_default_id', INTEGER(unsigned=True),
           ForeignKey('net_default_maps.net_default_id', ondelete='cascade'),
           nullable=False),
    Column(u'vlan_id', INTEGER(),
           ForeignKey('vlans.VlanID', ondelete='cascade'),
           nullable=False),
    UniqueConstraint(u'net_default_id', u'vlan_id', name='trunk_key'),
    mysql_engine='InnoDB', mysql_charset='utf8',
)
