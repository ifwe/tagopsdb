from elixir import Field, Integer
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

    ## TODO: correctly define class with these relationships:
    # belongs_to(
    #     'project',
    #     of_kind='Projects',
    #     colname='project_id',
    #     ondelete='cascade',
    #     primary_key=True
    # )
    # belongs_to(
    #     'package_definition',
    #     of_kind='PackageDefinitions',
    #     colname='pkg_def_id',
    #     ondelete='cascade',
    #     primary_key=True
    # )
    # belongs_to(
    #     'app',
    #     of_kind='AppDefinitions',
    #     colname='app_id',
    #     ondelete='cascade',
    #     primary_key=True
    # )
