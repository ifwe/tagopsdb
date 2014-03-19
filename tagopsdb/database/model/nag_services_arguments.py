from sqlalchemy import Column, ForeignKey, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base

from .nag_command_arguments import NagCommandArguments
from .nag_services import NagServices


class NagServicesArguments(Base):
    __tablename__ = 'nag_services_arguments'

    service_id = Column(INTEGER(),
                        ForeignKey(NagServices.id, ondelete='cascade'),
                        primary_key=True)
    command_argument_id = Column(INTEGER(),
                                 ForeignKey(NagCommandArguments.id,
                                            ondelete='cascade'),
                                 primary_key=True)
    value = Column(VARCHAR(length=120), nullable=False)

    command_argument = relationship(
        'NagCommandArguments',
        backref='nag_services_assoc'
    )
