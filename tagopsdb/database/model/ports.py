from sqlalchemy import Column, UniqueConstraint, ForeignKey, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base

from .network_device import NetworkDevice


class Ports(Base):
    __tablename__ = 'ports'

    id = Column(u'PortID', INTEGER(), primary_key=True)
    network_id = Column(u'NetworkID', INTEGER(),
                        ForeignKey(NetworkDevice.id, ondelete='cascade'))
    port_number = Column(u'portNumber', VARCHAR(length=20))
    description = Column(VARCHAR(length=50))
    speed = Column(VARCHAR(length=20))
    duplex = Column(VARCHAR(length=20))

    network_interface = relationship('HostInterfaces', uselist=False)

    __table_args__ = (
        UniqueConstraint('NetworkID', 'portNumber',
                         name='NetworkID_portNumber'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'},
    )

    def __init__(self, network_id, port_number, description, speed, duplex):
        """ """

        self.network_id = network_id
        self.port_number = port_number
        self.description = description
        self.speed = speed
        self.duplex = duplex
