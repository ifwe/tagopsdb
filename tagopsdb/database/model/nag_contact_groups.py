from elixir import Field, String, Integer, using_options

from .base import Base


class NagContactGroups(Base):
    using_options(tablename='nag_contact_groups')

    id = Field(Integer, primary_key=True)
    name = Field(String(length=32), nullable=False, unique=True)
    alias = Field(String(length=80))
