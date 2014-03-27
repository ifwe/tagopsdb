from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base


class Zones(Base):
    __tablename__ = 'zones'

    id = Column(u'ZoneID', INTEGER(), primary_key=True)
    zone_name = Column(u'zoneName', VARCHAR(length=30))
    mx_priority = Column(u'mxPriority', INTEGER())
    mx_host_id = Column(u'mxHostID', VARCHAR(length=30))
    ns_priority = Column(u'nsPriority', INTEGER())
    nameserver = Column(VARCHAR(length=30))

    cnames = relationship('Cname', backref='zone')

    def __init__(self, zone_name, mx_priority, mx_host_id, ns_priority,
                 nameserver):
        """ """

        self.zone_name = zone_name
        self.mx_priority = mx_priority
        self.mx_host_id = mx_host_id
        self.ns_priority = ns_priority
        self.nameserver = nameserver
