from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from sqlalchemy.orm import relationship

from .base import Base


class NsService(Base):
    __tablename__ = 'ns_service'

    id = Column(u'serviceID', INTEGER(unsigned=True), primary_key=True)
    service_name = Column(u'serviceName', VARCHAR(length=64), nullable=False,
                          unique=True)
    proto = Column(VARCHAR(length=16), nullable=False)
    port = Column(SMALLINT(display_width=5, unsigned=True), nullable=False)

    ns_monitors = relationship('NsMonitor', secondary='ns_service_binds')
    service_params = relationship('NsServiceParams')

    def __init__(self, service_name, proto, port):
        """ """

        self.service_name = service_name
        self.proto = proto
        self.port = port
