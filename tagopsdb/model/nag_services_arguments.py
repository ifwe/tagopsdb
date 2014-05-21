from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class NagServicesArguments(Base):
    __tablename__ = 'nag_services_arguments'

    service_id = Column(
        INTEGER(),
        ForeignKey('nag_services.id', ondelete='cascade'),
        primary_key=True
    )
    command_argument_id = Column(
        INTEGER(),
        ForeignKey('nag_command_arguments.id', ondelete='cascade'),
        primary_key=True
    )
    value = Column(String(length=120), nullable=False)
    command_argument = relationship(
        'NagCommandArgument',
        backref='nag_services_assoc'
    )
