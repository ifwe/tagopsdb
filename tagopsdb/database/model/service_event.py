from sqlalchemy import Column, ForeignKey, TIMESTAMP, VARCHAR, TEXT
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.sql.expression import func

from .base import Base

from .hosts import Hosts


class ServiceEvent(Base):
    __tablename__ = 'serviceEvent'

    id = Column(u'ServiceID', INTEGER(), primary_key=True)
    host_id = Column(u'HostID', INTEGER(),
                     ForeignKey(Hosts.id, ondelete='cascade'))
    user = Column(VARCHAR(length=20))
    service_status = Column(u'serviceStatus', VARCHAR(length=100))
    power_status = Column(u'powerStatus', VARCHAR(length=10))
    vendor_ticket = Column(u'vendorTicket', VARCHAR(length=20))
    comments = Column(TEXT())
    service_date = Column(u'serviceDate', TIMESTAMP(), nullable=False,
                          default=func.current_timestamp(),
                          onupdate=func.current_timestamp(),
                          server_onupdate=func.current_timestamp())

    def __init__(self, host_id, user, service_status, power_status,
                 vendor_ticket, comments, service_date):
        """ """

        self.host_id = host_id
        self.user = user
        self.service_status = service_status
        self.power_status = power_status
        self.vendor_ticket = vendor_ticket
        self.comments = comments
        self.service_date = service_date
