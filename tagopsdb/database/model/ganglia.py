from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base


class Ganglia(Base):
    __tablename__ = 'ganglia'

    id = Column(u'GangliaID', INTEGER(), primary_key=True)
    cluster_name = Column(VARCHAR(length=50))
    port = Column(INTEGER(display_width=5), nullable=False, default='8649',
                  server_default='8649')

    app_definitions = relationship('AppDefinitions')

    def __init__(self, cluster_name, port):
        """ """

        self.cluster_name = cluster_name
        self.port = port
