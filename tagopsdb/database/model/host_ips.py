from sqlalchemy import Column, ForeignKey, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base

from .host_interfaces import HostInterfaces
from .subnet import Subnet


class HostIps(Base):
    __tablename__ = 'host_ips'

    id = Column(u'IpID', INTEGER(), primary_key=True)
    interface_id = Column(u'InterfaceID', INTEGER(),
                          ForeignKey(HostInterfaces.id, ondelete='cascade'),
                          nullable=False, index=True)
    subnet_id = Column(u'SubnetID', INTEGER(),
                       ForeignKey(Subnet.id, ondelete='cascade'),
                       nullable=False, unique=True, index=True)
    priority = Column(INTEGER(unsigned=True), nullable=False, default=1,
                      server_default='1')
    a_record = Column(u'ARecord', VARCHAR(length=200))
    comments = Column(VARCHAR(length=200))

    subnet = relationship('Subnet', uselist=False, backref='host_ip')

    def __init__(self, interface_id, subnet_id, priority, a_record, comments):
        """ """

        self.interface_id = interface_id
        self.subnet_id = subnet_id
        self.priority = priority
        self.a_record = a_record
        self.comments = comments
