from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship

from .meta import Base, Column, String, SurrogatePK


class NagService(SurrogatePK, Base):
    __tablename__ = 'nag_services'

    check_command_id = Column(
        INTEGER(),
        ForeignKey('nag_check_commands.id', ondelete='cascade'),
        nullable=False
    )
    description = Column(String(length=255), nullable=False)
    max_check_attempts = Column(INTEGER(), nullable=False)
    check_interval = Column(INTEGER(), nullable=False)
    check_period_id = Column(
        INTEGER(),
        ForeignKey('nag_time_periods.id', ondelete='cascade'),
        nullable=False
    )
    retry_interval = Column(INTEGER(), nullable=False)
    notification_interval = Column(INTEGER(), nullable=False)
    notification_period_id = Column(
        INTEGER(),
        ForeignKey('nag_time_periods.id', ondelete='cascade'),
        nullable=False
    )
    applications = relationship('NagApptypesServices')
    check_period = relationship(
        'NagTimePeriod',
        foreign_keys=[ check_period_id ],
        uselist=False
    )
    command_arguments = relationship(
        'NagServicesArguments',
        backref='nag_services'
    )
    contact_groups = relationship(
        'NagContactGroup',
        secondary='nag_services_contact_groups',
        backref='nag_services'
    )
    contacts = relationship(
        'NagContact',
        secondary='nag_services_contacts',
        backref='nag_services'
    )
    environments = relationship('NagApptypesServices')
    hosts = relationship('NagHostsServices')
    nag_check_command = relationship(
        'NagCheckCommand',
        uselist=False,
        backref='nag_services'
    )
    notification_period = relationship(
        'NagTimePeriod',
        foreign_keys=[ notification_period_id ],
        uselist=False
    )
