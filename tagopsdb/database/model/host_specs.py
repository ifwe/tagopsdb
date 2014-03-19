from sqlalchemy import Column, Enum, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, BOOLEAN, MEDIUMTEXT

from sqlalchemy.orm import relationship

from .base import Base


class HostSpecs(Base):
    __tablename__ = 'host_specs'

    id = Column(u'specID', INTEGER(), primary_key=True)
    gen = Column(VARCHAR(length=4))
    memory_size = Column(u'memorySize', INTEGER(display_width=4))
    cores = Column(SMALLINT(display_width=2), nullable=False)
    cpu_speed = Column(u'cpuSpeed', INTEGER(display_width=6))
    disk_size = Column(u'diskSize', INTEGER(display_width=6))
    vendor = Column(VARCHAR(length=20))
    model = Column(VARCHAR(length=20))
    control = Column(Enum(u'digi', u'ipmi', u'libvirt', u'vmware'))
    virtual = Column(BOOLEAN(), nullable=False, default=0, server_default='0')
    expansions = Column(MEDIUMTEXT())

    services = relationship('NsServiceMax')

    def __init__(self, gen, memory_size, cores, cpu_speed, disk_size, vendor,
                 model, control, virtual, expansions):
        """ """

        self.gen = gen
        self.memory_size = memory_size
        self.cores = cores
        self.cpu_speed = cpu_speed
        self.disk_size = disk_size
        self.vendor = vendor
        self.model = model
        self.control = control
        self.virtual = virtual
        self.expansions = expansions
