from elixir import Field
from elixir import String, Integer
from elixir import using_options, using_table_options
from elixir import belongs_to, has_and_belongs_to_many

from .base import Base


class NagServices(Base):
    using_options(tablename='nag_services')
    using_table_options(extend_existing=True)

    id = Field(Integer, primary_key=True)
    description = Field(String(length=255), required=True)
    max_check_attempts = Field(Integer, required=True)
    check_interval = Field(Integer, required=True)
    retry_interval = Field(Integer, required=True)
    notification_interval = Field(Integer, required=True)

    belongs_to(
        'check_command',
        of_kind='NagCheckCommands',
        colname='check_command_id',
        ondelete='cascade',
        required=True,
    )

    belongs_to(
        'check_period',
        of_kind='NagTimePeriods',
        colname='check_period_id',
        ondelete='cascade',
        required=True,
    )

    belongs_to(
        'notification_period',
        of_kind='NagTimePeriods',
        colname='notification_period_id',
        ondelete='cascade',
        required=True,
    )
