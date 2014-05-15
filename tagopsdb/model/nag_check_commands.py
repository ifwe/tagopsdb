from sqlalchemy.orm import relationship

from .meta import Base, Column, String, SurrogatePK


class NagCheckCommand(SurrogatePK, Base):
    __tablename__ = 'nag_check_commands'

    command_name = Column(String(length=32), nullable=False, unique=True)
    command_line = Column(String(length=255), nullable=False)
    nag_command_arguments = relationship('NagCommandArgument')
