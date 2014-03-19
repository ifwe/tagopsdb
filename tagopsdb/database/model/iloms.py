from sqlalchemy import Column, ForeignKey, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base

from .hosts import Hosts
from .ports import Ports
from .subnet import Subnet


class Iloms(Base):
    __tablename__ = 'iloms'

    id = Column(u'ILomID', INTEGER(), primary_key=True)
    host_id = Column(u'HostID', INTEGER(),
                     ForeignKey(Hosts.id, ondelete='cascade'),
                     unique=True, index=True)
    subnet_id = Column(u'SubnetID', INTEGER(),
                       ForeignKey(Subnet.id, ondelete='cascade'),
                       nullable=False, unique=True, index=True)
    mac_address = Column(u'macAddress', VARCHAR(length=18), unique=True)
    port_id = Column(u'PortID', INTEGER(),
                     ForeignKey(Ports.id, ondelete='cascade'),
                     unique=True, index=True)
    a_record = Column(u'ARecord', VARCHAR(length=200))
    comments = Column(VARCHAR(length=200))

    # XXX: should this be Ports with backref='ilom' ?
    port = relationship('Subnet', uselist=False, backref='port')
    subnet = relationship('Subnet', uselist=False, backref='ilom')

    def __init__(self, host_id, subnet_id, mac_address, port_id, a_record,
                 comments):
        """ """

        self.host_id = host_id
        self.subnet_id = subnet_id
        self.mac_address = mac_address
        self.port_id = port_id
        self.a_record = a_record
        self.comments = comments
