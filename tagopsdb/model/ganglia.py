from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Ganglia(Base):
    __tablename__ = 'ganglia'

    id = Column(u'GangliaID', INTEGER(), primary_key=True)
    cluster_name = Column(String(length=50))
    port = Column(
        INTEGER(display_width=5),
        nullable=False,
        server_default='8649'
    )
    app_definitions = relationship('AppDefinition')
