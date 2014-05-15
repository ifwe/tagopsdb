from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, TEXT, TIMESTAMP
from sqlalchemy.sql.expression import func

from .meta import Base, Column, String


class ServiceEvent(Base):
    __tablename__ = 'serviceEvent'

    id = Column(u'ServiceID', INTEGER(), primary_key=True)
    host_id = Column(
        u'HostID',
        INTEGER(),
        ForeignKey('hosts.HostID', ondelete='cascade')
    )
    user = Column(String(length=20))
    service_status = Column(u'serviceStatus', String(length=100))
    power_status = Column(u'powerStatus', String(length=10))
    vendor_ticket = Column(u'vendorTicket', String(length=20))
    comments = Column(TEXT())
    service_date = Column(
        u'serviceDate',
        TIMESTAMP(),
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        server_onupdate=func.current_timestamp()
    )
