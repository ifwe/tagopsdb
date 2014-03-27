from sqlalchemy import Column, UniqueConstraint, ForeignKey, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base

from .nag_check_commands import NagCheckCommands


class NagCommandArguments(Base):
    __tablename__ = 'nag_command_arguments'

    id = Column(INTEGER(), primary_key=True)
    check_command_id = Column(INTEGER(),
                              ForeignKey(NagCheckCommands.id,
                                         ondelete='cascade'),
                              nullable=False)
    label = Column(VARCHAR(length=32), nullable=False)
    description = Column(VARCHAR(length=255), nullable=False)
    arg_order = Column(INTEGER(), nullable=False)
    default_value = Column(VARCHAR(length=80))

    __table_args__ = (
        UniqueConstraint(u'check_command_id', u'arg_order',
                         name='check_command_arg_order'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'},
    )
