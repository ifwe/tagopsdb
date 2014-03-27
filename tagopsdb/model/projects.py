from elixir import Field
from elixir import String, Integer
from elixir import using_options, has_and_belongs_to_many

from .base import Base


class Projects(Base):
    using_options(tablename='projects')

    id = Field(Integer, colname='project_id', primary_key=True)
    name = Field(String(length=255), required=True, unique=True)
    has_and_belongs_to_many(
        'package_definitions',
        of_kind='PackageDefinitions',
        inverse='projects',
        tablename='project_package',
        local_colname='project_id',
        remote_colname='pkg_def_id',
        table_kwargs=dict(extend_existing=True)
    )

    has_and_belongs_to_many(
        'apps',
        of_kind='Application',
        inverse='projects',
        tablename='project_package',
        local_colname='project_id',
        remote_colname='app_id',
        table_kwargs=dict(extend_existing=True)
    )
