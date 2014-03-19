from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base


class NetworkDevice(Base):
    __tablename__ = 'networkDevice'

    id = Column(u'NetworkID', INTEGER(), primary_key=True)
    system_name = Column(u'systemName', VARCHAR(length=20), unique=True)
    model = Column(VARCHAR(length=50))
    hardware_code = Column(u'hardwareCode', VARCHAR(length=20))
    software_code = Column(u'softwareCode', VARCHAR(length=20))

    host_interface = relationship(
        'HostInterfaces',
        uselist=False,
    )
    ports = relationship('Ports')

    def __init__(self, system_name, model, hardware_code, software_code):
        """ """

        self.system_name = system_name
        self.model = model
        self.hardware_code = hardware_code
        self.software_code = software_code
