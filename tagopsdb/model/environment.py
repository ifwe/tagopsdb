from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Environment(Base):
    __tablename__ = 'environments'

    id = Column(u'environmentID', INTEGER(), primary_key=True)
    environment = Column(String(length=15), nullable=False, unique=True)
    env = Column(String(length=12), nullable=False, unique=True)
    domain = Column(String(length=32), nullable=False, unique=True)
    prefix = Column(String(length=1), nullable=False)
    zone_id = Column(INTEGER(), ForeignKey('zones.ZoneID'), nullable=False)
    zone = relationship('Zone', uselist=False)
