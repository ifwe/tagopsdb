from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from .meta import Base, Column


class NsWeight(Base):
    __tablename__ = 'ns_weight'

    vip_id = Column(
        u'vipID',
        INTEGER(unsigned=True),
        ForeignKey('ns_vip.vipID', ondelete='cascade'),
        primary_key=True
    )
    spec_id = Column(
        u'specID',
        INTEGER(),
        ForeignKey('host_specs.specID', ondelete='cascade'),
        primary_key=True
    )
    weight = Column(TINYINT(display_width=3, unsigned=True), nullable=False)
    host_spec = relationship('NsVip', uselist=False, backref='ns_vip_assocs')
