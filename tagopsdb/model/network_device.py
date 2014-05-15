from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class NetworkDevice(Base):
    __tablename__ = 'networkDevice'

    id = Column(u'NetworkID', INTEGER(), primary_key=True)
    system_name = Column(u'systemName', String(length=20), unique=True)
    model = Column(String(length=50))
    hardware_code = Column(u'hardwareCode', String(length=20))
    software_code = Column(u'softwareCode', String(length=20))
    host_interface = relationship('HostInterface', uselist=False)
    ports = relationship('Port')
