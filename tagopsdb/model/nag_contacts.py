from elixir import Field
from elixir import String, Integer
from elixir import using_options

from .base import Base


class NagContacts(Base):
    using_options(tablename='nag_contacts')

    id = Field(Integer, primary_key=True)
    name = Field(String(length=32), required=True, unique=True)
    alias = Field(String(length=80))
    email = Field(String(length=80))
    pager = Field(String(length=80))
