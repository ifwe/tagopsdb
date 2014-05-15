from sqlalchemy import Enum
from sqlalchemy.dialects.mysql import BOOLEAN, INTEGER, MEDIUMTEXT, SMALLINT
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class HostSpec(Base):
    __tablename__ = 'host_specs'

    id = Column(u'specID', INTEGER(), primary_key=True)
    gen = Column(String(length=4))
    memory_size = Column(u'memorySize', INTEGER(display_width=4))
    cores = Column(SMALLINT(display_width=2), nullable=False)
    cpu_speed = Column(u'cpuSpeed', INTEGER(display_width=6))
    disk_size = Column(u'diskSize', INTEGER(display_width=6))
    vendor = Column(String(length=20))
    model = Column(String(length=20))
    control = Column(Enum(u'digi', u'ipmi', u'libvirt', u'vmware'))
    virtual = Column(BOOLEAN(), nullable=False, server_default='0')
    expansions = Column(MEDIUMTEXT())
    services = relationship('NsServiceMax')
