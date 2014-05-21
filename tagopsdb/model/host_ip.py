from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class HostIp(Base):
    __tablename__ = 'host_ips'

    id = Column(u'IpID', INTEGER(), primary_key=True)
    interface_id = Column(
        u'InterfaceID',
        INTEGER(),
        ForeignKey('host_interfaces.InterfaceID', ondelete='cascade'),
        nullable=False,
        index=True
    )
    subnet_id = Column(
        u'SubnetID',
        INTEGER(),
        ForeignKey('subnet.SubnetID', ondelete='cascade'),
        nullable=False,
        unique=True,
        index=True
    )
    priority = Column(
        INTEGER(unsigned=True),
        nullable=False,
        server_default='1'
    )
    a_record = Column(u'ARecord', String(length=200))
    comments = Column(String(length=200))
    subnet = relationship('Subnet', uselist=False, backref='host_ip')
