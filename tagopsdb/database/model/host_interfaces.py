from sqlalchemy import Column, UniqueConstraint, ForeignKey, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base


class HostInterfaces(Base):
    __tablename__ = 'host_interfaces'

    id = Column(u'InterfaceID', INTEGER(), primary_key=True)
    host_id = Column(u'HostID', INTEGER(),
                     ForeignKey('hosts.HostID', ondelete='cascade'),
                     index=True)
    network_id = Column(
        u'NetworkID',
        INTEGER(),
        ForeignKey('networkDevice.NetworkID', ondelete='cascade'),
        index=True
    )
    interface_name = Column(u'interfaceName', VARCHAR(length=10))
    mac_address = Column(u'macAddress', VARCHAR(length=18), unique=True)
    port_id = Column(u'PortID', INTEGER(), ForeignKey('ports.PortID'),
                     unique=True, index=True)

    host_ips = relationship('HostIps', backref='host_interface')

    __table_args__ = (
        UniqueConstraint(u'HostID', u'interfaceName'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'},
    )

    def __init__(self, host_id, network_id, interface_name, mac_address,
                 port_id):
        """ """

        self.host_id = host_id
        self.network_id = network_id
        self.interface_name = interface_name
        self.mac_address = mac_address
        self.port_id = port_id
