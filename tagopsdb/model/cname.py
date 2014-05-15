from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Cname(Base):
    __tablename__ = 'cname'

    id = Column(u'CnameID', INTEGER(), primary_key=True)
    name = Column(String(length=40))
    ip_id = Column(
        u'IpID',
        INTEGER(),
        ForeignKey('host_ips.IpID', onupdate='cascade',
        ondelete='cascade')
    )
    zone_id = Column(
        u'ZoneID',
        INTEGER(),
        ForeignKey('zones.ZoneID', onupdate='cascade', ondelete='cascade')
    )
    host = relationship('HostIp', uselist=False)

    __table_args__ = (
        UniqueConstraint(u'name', u'ZoneID', name=u'name_ZoneID'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
