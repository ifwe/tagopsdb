from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base


class JmxAttributes(Base):
    __tablename__ = 'jmx_attributes'

    id = Column(u'jmx_attribute_id', INTEGER(), primary_key=True)
    obj = Column(VARCHAR(length=300), nullable=False)
    attr = Column(VARCHAR(length=300), nullable=False)
    g_group_name = Column(u'GgroupName', VARCHAR(length=25))
