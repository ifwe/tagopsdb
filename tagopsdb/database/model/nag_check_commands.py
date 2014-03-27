from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base


class NagCheckCommands(Base):
    __tablename__ = 'nag_check_commands'

    id = Column(INTEGER(), primary_key=True)
    command_name = Column(VARCHAR(length=32), nullable=False, unique=True)
    command_line = Column(VARCHAR(length=255), nullable=False)
    nag_command_arguments = relationship('NagCommandArguments')
