from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import DATE, INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Asset(Base):
    __tablename__ = 'asset'

    id = Column(u'AssetID', INTEGER(), primary_key=True)
    host_id = Column(
        u'HostID',
        INTEGER(),
        ForeignKey('hosts.HostID', ondelete='cascade'),
        nullable=False
    )
    oem_serial = Column(u'oemSerial', String(length=30), unique=True)
    service_tag = Column(u'serviceTag', String(length=20))
    tagged_serial = Column(u'taggedSerial', String(length=20))

    host = relationship('Host', uselist=False)
