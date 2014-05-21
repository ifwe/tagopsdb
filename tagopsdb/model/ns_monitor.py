from sqlalchemy.dialects.mysql import INTEGER

from .meta import Base, Column, String


class NsMonitor(Base):
    __tablename__ = 'ns_monitor'

    id = Column(u'monitorID', INTEGER(unsigned=True), primary_key=True)
    monitor = Column(String(length=32), nullable=False, unique=True)
