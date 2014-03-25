from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to
from sqlalchemy import ForeignKey

from .base import Base


class PackageNames(Base):
    using_options(tablename='package_names')

    id = Field(Integer, colname='pkg_name_id', primary_key=True)
    name = Field(String(length=255), nullable=False)
    pkg_def_id = Field(Integer, ForeignKey('package_definitions.pkg_def_id'))
    # belongs_to(
    #     'package_definition',
    #     of_kind='PackageDefinitions',
    #     field=pkg_def_id
    # )
