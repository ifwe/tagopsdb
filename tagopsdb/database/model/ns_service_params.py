from sqlalchemy import Column, ForeignKey, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base

from .ns_service import NsService


class NsServiceParams(Base):
    __tablename__ = 'ns_service_params'

    service_id = Column(u'serviceID', INTEGER(unsigned=True),
                        ForeignKey(NsService.id, ondelete='cascade'),
                        primary_key=True)
    param = Column(VARCHAR(length=32), primary_key=True)
    value = Column(VARCHAR(length=128), nullable=False)

    def __init__(self, service_id, param, value):
        """ """

        self.service_id = service_id
        self.param = param
        self.value = value
