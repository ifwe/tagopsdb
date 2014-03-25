from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to

from .base import Base


class NagServices(Base):
    using_options(tablename='nag_services')

    id = Field(Integer, primary_key=True)
    description = Field(String(length=255), nullable=False)
    max_check_attempts = Field(Integer, nullable=False)
    check_interval = Field(Integer, nullable=False)
    retry_interval = Field(Integer, nullable=False)
    notification_interval = Field(Integer, nullable=False)

    belongs_to(
        'check_command',
        of_kind='NagCheckCommands',
        colname='check_command_id'
    )
    belongs_to(
        'check_period',
        of_kind='NagTimePeriods',
        colname='check_period_id'
    )
    belongs_to(
        'notification_period',
        of_kind='NagTimePeriods',
        colname='notification_period_id'
    )
