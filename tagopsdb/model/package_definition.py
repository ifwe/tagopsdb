from elixir import Field
from elixir import String, Integer, Enum
from elixir import using_options, has_many, has_and_belongs_to_many
from sqlalchemy.dialects.mysql import TINYINT, TIMESTAMP
from sqlalchemy.sql.expression import func

from .base import Base


class PackageDefinition(Base):
    using_options(tablename='package_definitions')

    id = Field(Integer, colname='pkg_def_id', primary_key=True)
    deploy_type = Field(String(length=30), required=True)
    validation_type = Field(String(length=15), required=True)
    name = Field(String(length=255), colname='pkg_name', required=True)

    path = Field(String(length=255), required=True)
    arch = Field(
        String(length=6),
        Enum(u'i386', u'x86_64', u'noarch'),
        required=True,
        default='noarch',
        server_default='noarch'
    )

    build_type = Field(
        Enum('developer', 'hudson', 'jenkins'),
        required=True,
        default='developer',
        server_default='developer'
    )

    build_host = Field(String(length=255), required=True)
    env_specific = Field(
        TINYINT(1),
        required=True,
        default=0,
        server_default='0'
    )

    created = Field(
        TIMESTAMP,
        required=True,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
    )

    has_many('versions', of_kind='Package', inverse='definition')

    has_and_belongs_to_many(
        'projects',
        of_kind='Project',
        inverse='package_definitions',
        tablename='project_package',
        local_colname='pkg_def_id',
        remote_colname='project_id',
        table_kwargs=dict(extend_existing=True)
    )

    has_and_belongs_to_many(
        'apps',
        of_kind='Application',
        inverse='package_definitions',
        tablename='project_package',
        local_colname='pkg_def_id',
        remote_colname='app_id',
        table_kwargs=dict(extend_existing=True)
    )

    has_many(
        'package_names',
        of_kind='PackageName',
        inverse='package_definition'
    )