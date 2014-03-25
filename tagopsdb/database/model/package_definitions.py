from elixir import Field
from elixir import String, Integer, Boolean, DateTime, Enum
from elixir import using_options, has_many, belongs_to, has_and_belongs_to_many
from sqlalchemy import ForeignKey
from sqlalchemy.sql.expression import func

from .base import Base


class PackageDefinitions(Base):
    using_options(tablename='package_definitions')

    id = Field(Integer, colname='pkg_def_id', primary_key=True)
    deploy_type = Field(String(length=30), nullable=False)
    validation_type = Field(String(length=15), nullable=False)
    pkg_name = Field(String(length=255), nullable=False)

    path = Field(String(length=255), nullable=False)
    arch = Field(
        String(length=6),
        Enum(u'i386', u'x86_64', u'noarch'),
        nullable=False,
        default='noarch',
        server_default='noarch'
    )

    build_type = Field(
        String(length=9),
        Enum('developer', 'hudson', 'jenkins'),
        nullable=False,
        default='developer',
        server_default='developer'
    )

    build_host = Field(String(length=255), nullable=False)
    env_specific = Field(
        Boolean,
        nullable=False,
        default=0,
        server_default='0'
    )

    created = Field(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
    )

    has_many('packages', of_kind='Packages')
    # has_many(
    #     'package_name',
    #     of_kind='PackageNames',
    # )
    has_and_belongs_to_many(
        'projects',
        of_kind='Projects',
        inverse='package_definitions',
        tablename='project_package',
        local_colname='pkg_def_id',
        remote_colname='project_id',
        table_kwargs=dict(extend_existing=True)
    )

    has_and_belongs_to_many(
        'app_definitions',
        of_kind='AppDefinitions',
        inverse='package_definitions',
        tablename='project_package',
        local_colname='pkg_def_id',
        remote_colname='app_id',
        table_kwargs=dict(extend_existing=True)
    )
