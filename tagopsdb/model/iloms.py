from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Ilom(Base):
    __tablename__ = 'iloms'

    id = Column(u'ILomID', INTEGER(), primary_key=True)
    host_id = Column(
        u'HostID',
        INTEGER(),
        ForeignKey('hosts.HostID', ondelete='cascade'),
        unique=True,
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
    mac_address = Column(u'macAddress', String(length=18), unique=True)
    port_id = Column(
        u'PortID',
        INTEGER(),
        ForeignKey('ports.PortID', ondelete='cascade'),
        unique=True,
        index=True
    )
    a_record = Column(u'ARecord', String(length=200))
    comments = Column(String(length=200))
    port = relationship('Subnet', uselist=False, backref='port')
    subnet = relationship('Subnet', uselist=False, backref='ilom')
