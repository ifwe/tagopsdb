from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Subnet(Base):
    __tablename__ = 'subnet'

    id = Column(u'SubnetID', INTEGER(), primary_key=True)
    vlan_id = Column(
        u'VlanID',
        INTEGER(),
        ForeignKey('vlans.VlanID', ondelete='cascade')
    )
    ip_address = Column(u'ipAddress', String(length=15), unique=True)
    netmask = Column(String(length=15))
    gateway = Column(String(length=15))
    zone_id = Column(u'ZoneID', INTEGER(), ForeignKey('zones.ZoneID'))
    zone = relationship('Zone', uselist=False, backref='subnets')
