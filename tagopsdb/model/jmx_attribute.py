from sqlalchemy.dialects.mysql import INTEGER

from .meta import Base, Column, String


class JmxAttribute(Base):
    __tablename__ = 'jmx_attributes'

    id = Column(u'jmx_attribute_id', INTEGER(), primary_key=True)
    obj = Column(String(length=300), nullable=False)
    attr = Column(String(length=300), nullable=False)
    g_group_name = Column(u'GgroupName', String(length=25))
