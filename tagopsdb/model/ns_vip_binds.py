from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship

from .meta import Base, Column


class NsVipBinds(Base):
    __tablename__ = 'ns_vip_binds'

    net_default_ip_id = Column(
        INTEGER(unsigned=True),
        ForeignKey('net_default_ips.net_default_ip_id', ondelete='cascade'),
        primary_key=True
    )
    vip_id = Column(
        u'vipID',
        INTEGER(unsigned=True),
        ForeignKey('ns_vip.vipID', ondelete='cascade'),
        primary_key=True
    )
    service_id = Column(
        u'serviceID',
        INTEGER(unsigned=True),
        ForeignKey('ns_service.serviceID', ondelete='cascade'),
        primary_key=True
    )
    ns_service = relationship('NsService')
    ns_vip = relationship('NsVip')
