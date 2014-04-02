from elixir import Field
from elixir import String, Integer
from elixir import using_options, has_many

from .base import Base


class NagCheckCommands(Base):
    using_options(tablename='nag_check_commands')

    id = Field(Integer, primary_key=True)
    command_name = Field(String(length=32), required=True, unique=True)
    command_line = Field(String(length=255), required=True)

    has_many(
        'arguments',
        of_kind='NagCommandArguments',
        inverse='check_command',
    )

    has_many(
        'services',
        of_kind='NagServices',
        inverse='check_command',
    )
