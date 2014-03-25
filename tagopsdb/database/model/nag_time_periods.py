from elixir import Field
from elixir import String, Integer
from elixir import using_options

from .base import Base


class NagTimePeriods(Base):
    using_options(tablename='nag_time_periods')

    id = Field(Integer, primary_key=True)
    name = Field(String(length=32), nullable=False, unique=True)
    alias = Field(String(length=80))
    sunday = Field(String(length=32))
    monday = Field(String(length=32))
    tuesday = Field(String(length=32))
    wednesday = Field(String(length=32))
    thursday = Field(String(length=32))
    friday = Field(String(length=32))
    saturday = Field(String(length=32))
