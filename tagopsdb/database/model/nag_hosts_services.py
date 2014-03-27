from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from sqlalchemy.orm import relationship

from .base import Base

from .hosts import Hosts
from .app_definitions import AppDefinitions
from .nag_services import NagServices


class NagHostsServices(Base):
    __tablename__ = 'nag_hosts_services'

    host_id = Column(INTEGER(), ForeignKey(Hosts.id, ondelete='cascade'),
                     primary_key=True)
    service_id = Column(INTEGER(),
                        ForeignKey(NagServices.id, ondelete='cascade'),
                        primary_key=True)
    server_app_id = Column(SMALLINT(display_width=6),
                           ForeignKey(AppDefinitions.id),
                           primary_key=True)

    host = relationship('Hosts')
    service = relationship('NagServices')
