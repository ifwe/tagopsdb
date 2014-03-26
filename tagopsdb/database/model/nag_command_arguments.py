from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to, using_table_options
from sqlalchemy import UniqueConstraint
from .base import Base


class NagCommandArguments(Base):
    using_options(tablename='nag_command_arguments')
    using_table_options(
        UniqueConstraint(
            'check_command_id',
            'arg_order',
            name='check_command_arg_order'
        )
    )

    id = Field(Integer, primary_key=True)
    label = Field(String(length=32), required=True)
    description = Field(String(length=255), required=True)
    arg_order = Field(Integer, required=True)
    default_value = Field(String(length=80))

    belongs_to(
        'check_command',
        of_kind='NagCheckCommands',
        colname='check_command_id',
        required=True,
        ondelete='cascade',
    )
