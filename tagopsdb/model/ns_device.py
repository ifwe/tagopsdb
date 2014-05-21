from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class NsDevice(Base):
    __tablename__ = 'ns_device'

    id = Column(u'deviceID', INTEGER(unsigned=True), primary_key=True)
    proto = Column(String(length=6), nullable=False)
    host = Column(String(length=32), nullable=False)
    vips = relationship('NsVip')

    __table_args__ = (
        UniqueConstraint(u'proto', u'host', name=u'proto_host'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
