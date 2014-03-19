from sqlalchemy import Column, UniqueConstraint, ForeignKey, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base

from .ns_device import NsDevice


class NsVip(Base):
    __tablename__ = 'ns_vip'

    id = Column(u'vipID', INTEGER(unsigned=True), primary_key=True)
    vserver = Column(VARCHAR(length=64), nullable=False)
    device_id = Column(u'deviceID', INTEGER(unsigned=True),
                       ForeignKey(NsDevice.id, ondelete='cascade'),
                       nullable=False)

    host_specs = relationship('NsWeight', backref='ns_vip')

    __table_args__ = (
        UniqueConstraint(u'deviceID', u'vserver', name=u'device_vserver'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'},
    )

    def __init__(self, vserver, device_id):
        """ """

        self.vserver = vserver
        self.device_id = device_id
