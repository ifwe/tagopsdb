from elixir import Field
from elixir import Integer
from elixir import using_options, using_table_options
from sqlalchemy import UniqueConstraint

from .base import Base


class ProjectPackage(Base):
    using_options(tablename='project_package')
    using_table_options(
        UniqueConstraint('project_id', 'pkg_def_id', 'app_id'),
        extend_existing=True
    )

    project_id = Field(Integer, primary_key=True)
    pkg_def_id = Field(Integer, primary_key=True)
    app_id = Field(Integer, primary_key=True)
