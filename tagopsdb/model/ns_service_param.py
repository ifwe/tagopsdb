from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

from .meta import Base, Column, String


class NsServiceParam(Base):
    __tablename__ = 'ns_service_params'

    service_id = Column(
        u'serviceID',
        INTEGER(unsigned=True),
        ForeignKey('ns_service.serviceID', ondelete='cascade'),
        primary_key=True
    )
    param = Column(String(length=32), primary_key=True)
    value = Column(String(length=128), nullable=False)
