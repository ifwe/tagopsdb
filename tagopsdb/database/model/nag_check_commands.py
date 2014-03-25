from elixir import Field
from elixir import String, Integer
from elixir import using_options

from .base import Base


class NagCheckCommands(Base):
    using_options(tablename='nag_check_commands')

    id = Field(Integer, primary_key=True)
    command_name = Field(String(length=32), nullable=False, unique=True)
    command_line = Field(String(length=255), nullable=False)
