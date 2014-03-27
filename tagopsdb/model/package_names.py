from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to, using_table_options
from sqlalchemy import UniqueConstraint

from .base import Base


class PackageNames(Base):
    using_options(tablename='package_names')
    using_table_options(
        UniqueConstraint(u'name', u'pkg_def_id', name='name_pkg_def_id'),
    )
    id = Field(Integer, colname='pkg_name_id', primary_key=True)
    name = Field(String(length=255), required=True)
    belongs_to(
        'package_definition',
        of_kind='PackageDefinition',
        colname='pkg_def_id',
        required=True,
        ondelete='cascade'
    )
