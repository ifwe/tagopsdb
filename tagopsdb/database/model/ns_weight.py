from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, TINYINT

from sqlalchemy.orm import relationship

from .base import Base

from .host_specs import HostSpecs
from .ns_vip import NsVip


class NsWeight(Base):
    __tablename__ = 'ns_weight'

    vip_id = Column(u'vipID', INTEGER(unsigned=True),
                    ForeignKey(NsVip.id, ondelete='cascade'),
                    primary_key=True)
    spec_id = Column(u'specID', INTEGER(),
                     ForeignKey(HostSpecs.id, ondelete='cascade'),
                     primary_key=True)
    weight = Column(TINYINT(display_width=3, unsigned=True), nullable=False)

    host_spec = relationship('NsVip', uselist=False, backref='ns_vip_assocs')

    def __init__(self, vip_id, spec_id, weight):
        """ """

        self.vip_id = vip_id
        self.spec_id = spec_id
        self.weight = weight
