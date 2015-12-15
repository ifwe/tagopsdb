from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class NetworkDevice(Base):
    __tablename__ = 'networkDevice'

    id = Column(u'NetworkID', INTEGER(), primary_key=True)
    system_name = Column(u'systemName', String(length=20), unique=True)
    host_interface = relationship('HostInterface', uselist=False)

    ports = relationship('Port')
