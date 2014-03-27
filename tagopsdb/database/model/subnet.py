from sqlalchemy import Column, ForeignKey, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base

from .vlans import Vlans
from .zones import Zones


class Subnet(Base):
    __tablename__ = 'subnet'

    id = Column(u'SubnetID', INTEGER(), primary_key=True)
    vlan_id = Column(u'VlanID', INTEGER(),
                     ForeignKey(Vlans.id, ondelete='cascade'))
    ip_address = Column(u'ipAddress', VARCHAR(length=15), unique=True)
    netmask = Column(VARCHAR(length=15))
    gateway = Column(VARCHAR(length=15))
    zone_id = Column(u'ZoneID', INTEGER(), ForeignKey(Zones.id))

    zone = relationship('Zones', uselist=False, backref='subnets')

    def __init__(self, vlan_id, ip_address, netmask, gateway, zone_id):
        """ """

        self.vlan_id = vlan_id
        self.ip_address = ip_address
        self.netmask = netmask
        self.gateway = gateway
        self.zone_id = zone_id
