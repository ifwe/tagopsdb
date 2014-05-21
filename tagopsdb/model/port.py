from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Port(Base):
    __tablename__ = 'ports'

    id = Column(u'PortID', INTEGER(), primary_key=True)
    network_id = Column(
        u'NetworkID',
        INTEGER(),
        ForeignKey('networkDevice.NetworkID', ondelete='cascade')
    )
    port_number = Column(u'portNumber', String(length=20))
    description = Column(String(length=50))
    speed = Column(String(length=20))
    duplex = Column(String(length=20))
    network_interface = relationship('HostInterface', uselist=False)

    __table_args__ = (
        UniqueConstraint('NetworkID', 'portNumber',
                         name='NetworkID_portNumber'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
