from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class HostInterface(Base):
    __tablename__ = 'host_interfaces'

    id = Column(u'InterfaceID', INTEGER(), primary_key=True)
    host_id = Column(
        u'HostID',
        INTEGER(),
        ForeignKey('hosts.HostID', ondelete='cascade'),
        index=True
    )
    network_id = Column(
        u'NetworkID',
        INTEGER(),
        ForeignKey('networkDevice.NetworkID', ondelete='cascade'),
        index = True
    )
    interface_name = Column(u'interfaceName', String(length=10))
    mac_address = Column(u'macAddress', String(length=18), unique=True)
    port_id = Column(
        u'PortID',
        INTEGER(),
        ForeignKey('ports.PortID'),
        unique=True,
        index=True
    )
    host_ips = relationship('HostIp', backref='host_interface')

    __table_args__ = (
        UniqueConstraint(u'HostID', u'interfaceName'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
