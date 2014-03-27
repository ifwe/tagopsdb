from sqlalchemy import Column, ForeignKey, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base


class NagServices(Base):
    __tablename__ = 'nag_services'

    id = Column(INTEGER(), primary_key=True)
    check_command_id = Column(INTEGER(),
                              ForeignKey('nag_check_commands.id',
                                         ondelete='cascade'),
                              nullable=False)
    description = Column(VARCHAR(length=255), nullable=False)
    max_check_attempts = Column(INTEGER(), nullable=False)
    check_interval = Column(INTEGER(), nullable=False)
    check_period_id = Column(INTEGER(),
                             ForeignKey('nag_time_periods.id',
                                        ondelete='cascade'),
                             nullable=False)
    retry_interval = Column(INTEGER(), nullable=False)
    notification_interval = Column(INTEGER(), nullable=False)
    notification_period_id = Column(INTEGER(),
                                    ForeignKey('nag_time_periods.id',
                                               ondelete='cascade'),
                                    nullable=False)

    applications = relationship('NagApptypesServices')
    check_period = relationship(
        'NagTimePeriods',
        foreign_keys=[check_period_id],
        uselist=False
    )
    command_arguments = relationship(
        'NagServicesArguments',
        backref='nag_services'
    )
    contact_groups = relationship(
        'NagContactGroups',
        secondary='nag_services_contact_groups',
        backref='nag_services'
    )
    contacts = relationship(
        'NagContacts',
        secondary='nag_services_contacts',
        backref='nag_services'
    )
    environments = relationship('NagApptypesServices')
    hosts = relationship('NagHostsServices')
    nag_check_command = relationship(
        'NagCheckCommands',
        uselist=False,
        backref='nag_services'
    )
    notification_period = relationship(
        'NagTimePeriods',
        foreign_keys=[notification_period_id],
        uselist=False
    )
