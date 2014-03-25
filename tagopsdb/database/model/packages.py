from elixir import Field
from elixir import String, Integer, DateTime, Enum
from elixir import using_options, belongs_to, has_many
from sqlalchemy.sql.expression import func

from .base import Base


class Packages(Base):
    using_options(tablename='packages')

    id = Field(Integer, colname='package_id', primary_key=True)
    version = Field(String(length=63), nullable=False)
    revision = Field(String(length=63), nullable=False)
    creator = Field(String(length=255), nullable=False)
    status = Field(
        Enum('completed', 'failed', 'pending', 'processing', 'removed'),
        nullable=False
    )
    created = Field(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
    )

    builder = Field(
        Enum('developer', 'hudson', 'jenkins'),
        nullable=False,
        default='developer',
        server_default='developer'
    )

    project_type = Field(
        Enum(u'application', u'kafka-config', u'tagconfig'),
        nullable=False,
        default='application',
        server_default='application'
    )

    belongs_to(
        'name',
        of_kind='PackageNames',
        colname='pkg_name',
        target_column='name',
    )

    belongs_to(
        'definition',
        of_kind='PackageDefinitions',
        colname='pkg_def_id'
    )

    has_many('deployments', of_kind='Deployments', inverse='package')
