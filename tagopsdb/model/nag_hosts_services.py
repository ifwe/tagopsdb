from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship

from .meta import Base, Column


class NagHostsServices(Base):
    __tablename__ = 'nag_hosts_services'

    host_id = Column(
        INTEGER(),
        ForeignKey('hosts.HostID', ondelete='cascade'),
        primary_key=True
    )
    service_id = Column(
        INTEGER(),
        ForeignKey('nag_services.id', ondelete='cascade'),
        primary_key=True
    )
    server_app_id = Column(
        SMALLINT(display_width=6),
        ForeignKey('app_definitions.AppID'),
        primary_key=True
    )
    host = relationship('Host')
    service = relationship('NagService')
