from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Zone(Base):
    __tablename__ = 'zones'

    id = Column(u'ZoneID', INTEGER(), primary_key=True)
    zone_name = Column(u'zoneName',String(length=30))

    cnames = relationship('Cname', backref='zone')
