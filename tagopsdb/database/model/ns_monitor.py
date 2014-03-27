from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base


class NsMonitor(Base):
    __tablename__ = 'ns_monitor'

    id = Column(u'monitorID', INTEGER(unsigned=True), primary_key=True)
    monitor = Column(VARCHAR(length=32), nullable=False, unique=True)

    def __init__(self, monitor):
        """ """

        self.monitor = monitor
