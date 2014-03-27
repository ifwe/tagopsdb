from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from sqlalchemy.orm import relationship

from .base import Base

from .environments import Environments
from .app_definitions import AppDefinitions
from .ns_service import NsService
from .ns_vip import NsVip


class NsVipBinds(Base):
    __tablename__ = 'ns_vip_binds'

    app_id = Column(u'appID', SMALLINT(display_width=6),
                    ForeignKey(AppDefinitions.id, ondelete='cascade'),
                    primary_key=True)
    vip_id = Column(u'vipID', INTEGER(unsigned=True),
                    ForeignKey(NsVip.id, ondelete='cascade'),
                    primary_key=True)
    service_id = Column(u'serviceID', INTEGER(unsigned=True),
                        ForeignKey(NsService.id, ondelete='cascade'),
                        primary_key=True)
    environment_id = Column(u'environmentID', INTEGER(),
                            ForeignKey(Environments.id, ondelete='cascade'),
                            primary_key=True)

    ns_service = relationship('NsService')
    ns_vip = relationship('NsVip')
