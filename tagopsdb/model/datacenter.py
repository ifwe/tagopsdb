from sqlalchemy.dialects.mysql import INTEGER

from .meta import Base, Column, String


class Datacenter(Base):
    __tablename__ = 'datacenters'

    id = Column(u'dc_id', INTEGER(), primary_key=True)

    dc_name = Column(String(length=32), unique=True, nullable=False)
    physical_location = Column(String(length=64), nullable=False)
    priority = Column(INTEGER(), nullable=False)
