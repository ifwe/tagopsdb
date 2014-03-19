from sqlalchemy import Column, UniqueConstraint, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base


class NsDevice(Base):
    __tablename__ = 'ns_device'

    id = Column(u'deviceID', INTEGER(unsigned=True), primary_key=True)
    proto = Column(VARCHAR(length=6), nullable=False)
    host = Column(VARCHAR(length=32), nullable=False)

    vips = relationship('NsVip')

    __table_args__ = (
        UniqueConstraint(u'proto', u'host', name=u'proto_host'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'},
    )

    def __init__(self, proto, host):
        """ """

        self.proto = proto
        self.host = host
