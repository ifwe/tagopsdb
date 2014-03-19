from sqlalchemy import Column, UniqueConstraint, ForeignKey, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base


class Cname(Base):
    __tablename__ = 'cname'

    id = Column(u'CnameID', INTEGER(), primary_key=True)
    name = Column(VARCHAR(length=40))
    ip_id = Column(u'IpID', INTEGER(),
                   ForeignKey('host_ips.IpID', onupdate='cascade',
                              ondelete='cascade'))
    zone_id = Column(u'ZoneID', INTEGER(),
                     ForeignKey('zones.ZoneID', onupdate='cascade',
                                ondelete='cascade'))

    host = relationship('HostIps', uselist=False)

    __table_args__ = (
        UniqueConstraint(u'name', u'ZoneID', name=u'name_ZoneID'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'},
    )

    def __init__(self, name, ip_id, zone_id):
        """ """

        self.name = name
        self.ip_id = ip_id
        self.zone_id = zone_id
