from elixir import Field
from elixir import String, Integer, DateTime, Enum
from elixir import using_options, belongs_to, has_many, using_table_options
from sqlalchemy.sql.expression import func
from sqlalchemy import UniqueConstraint

from .base import Base


class Package(Base):
    using_options(tablename='packages')
    using_table_options(
        UniqueConstraint(
            'pkg_name',
            'version',
            'revision',
            'builder',
            name='unique_package'
        ),
    )

    id = Field(Integer, colname='package_id', primary_key=True)
    version = Field(String(length=63), required=True)
    revision = Field(String(length=63), required=True)
    creator = Field(String(length=255), required=True)
    status = Field(
        Enum('completed', 'failed', 'pending', 'processing', 'removed'),
        required=True
    )
    created = Field(
        DateTime,
        required=True,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
    )

    builder = Field(
        Enum('developer', 'hudson', 'jenkins'),
        required=True,
        default='developer',
        server_default='developer'
    )

    project_type = Field(
        Enum(u'application', u'kafka-config', u'tagconfig'),
        required=True,
        default='application',
        server_default='application'
    )

    belongs_to(
        'name',
        of_kind='PackageName',
        colname='pkg_name',
        target_column='name',
        required=True,
    )

    belongs_to(
        'definition',
        of_kind='PackageDefinition',
        colname='pkg_def_id',
        required=True,
        ondelete='cascade'
    )

    has_many('deployments', of_kind='Deployment', inverse='package')
