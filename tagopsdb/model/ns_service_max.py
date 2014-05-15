from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column


class NsServiceMax(Base):
    __tablename__ = 'ns_service_max'

    spec_id = Column(
        u'specID',
        INTEGER(),
        ForeignKey('host_specs.specID', ondelete='cascade'),
        primary_key=True
    )
    service_id = Column(
        u'serviceID',
        INTEGER(unsigned=True),
        ForeignKey('ns_service.serviceID', ondelete='cascade'),
        primary_key=True
    )
    max_client = Column(
        u'maxClient',
        INTEGER(unsigned=True),
        nullable=False,
        server_default='0'
    )
    max_requests = Column(
        u'maxReq',
        INTEGER(unsigned=True),
        nullable=False,
        server_default='0'
    )
    service = relationship('NsService', uselist=False)
