from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class NsVip(Base):
    __tablename__ = 'ns_vip'

    id = Column(u'vipID', INTEGER(unsigned=True), primary_key=True)
    vserver = Column(String(length=64), nullable=False)
    device_id = Column(
        u'deviceID',
        INTEGER(unsigned=True),
        ForeignKey('ns_device.deviceID', ondelete='cascade'),
        nullable=False
    )
    host_specs = relationship('NsWeight', backref='ns_vip')

    __table_args__ = (
        UniqueConstraint(u'deviceID', u'vserver', name=u'device_vserver'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
