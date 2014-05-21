from sqlalchemy.dialects.mysql import SMALLINT, INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class NsService(Base):
    __tablename__ = 'ns_service'

    id = Column(u'serviceID', INTEGER(unsigned=True), primary_key=True)
    service_name = Column(
        u'serviceName',
        String(length=64),
        nullable=False,
        unique=True
    )
    proto = Column(String(length=16), nullable=False)
    port = Column(SMALLINT(display_width=5, unsigned=True), nullable=False)
    ns_monitors = relationship('NsMonitor', secondary='ns_service_binds')
    service_params = relationship('NsServiceParam')
