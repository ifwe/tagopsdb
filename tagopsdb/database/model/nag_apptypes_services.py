from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from sqlalchemy.orm import relationship

from .base import Base


class NagApptypesServices(Base):
    __tablename__ = 'nag_apptypes_services'

    app_id = Column(SMALLINT(display_width=2),
                    ForeignKey('app_definitions.AppID', ondelete='cascade'),
                    primary_key=True)
    service_id = Column(INTEGER(),
                        ForeignKey('nag_services.id', ondelete='cascade'),
                        primary_key=True)
    server_app_id = Column(SMALLINT(display_width=6),
                           ForeignKey('app_definitions.AppID'),
                           primary_key=True)
    environment_id = Column(
        INTEGER(),
        ForeignKey('environments.environmentID', ondelete='cascade'),
        primary_key=True
    )

    application = relationship('AppDefinitions', foreign_keys=[app_id])
    environment = relationship('Environments')
    service = relationship('NagServices')
