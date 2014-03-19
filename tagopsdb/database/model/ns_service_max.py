from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base

from .host_specs import HostSpecs
from .ns_service import NsService


class NsServiceMax(Base):
    __tablename__ = 'ns_service_max'

    spec_id = Column(u'specID', INTEGER(),
                     ForeignKey(HostSpecs.id, ondelete='cascade'),
                     primary_key=True)
    service_id = Column(u'serviceID', INTEGER(unsigned=True),
                        ForeignKey(NsService.id, ondelete='cascade'),
                        primary_key=True)
    max_client = Column(u'maxClient', INTEGER(unsigned=True), nullable=False,
                        default=0, server_default='0')
    max_requests = Column(u'maxReq', INTEGER(unsigned=True), nullable=False,
                          default=0, server_default='0')

    service = relationship('NsService', uselist=False)

    def __init__(self, spec_id, service_id, max_client, max_requests):
        """ """

        self.spec_id = spec_id
        self.service_id = service_id
        self.max_client = max_client
        self.max_requests = max_requests
