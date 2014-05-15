from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER

from .meta import Base, Column, String, SurrogatePK


class NagCommandArgument(SurrogatePK, Base):
    __tablename__ = 'nag_command_arguments'

    check_command_id = Column(
        INTEGER(),
        ForeignKey('nag_check_commands.id', ondelete='cascade'),
        nullable=False
    )
    label = Column(String(length=32), nullable=False)
    description = Column(String(length=255), nullable=False)
    arg_order = Column(INTEGER(), nullable=False)
    default_value = Column(String(length=80))

    __table_args__ = (
        UniqueConstraint(u'check_command_id', u'arg_order',
                         name='check_command_arg_order'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
