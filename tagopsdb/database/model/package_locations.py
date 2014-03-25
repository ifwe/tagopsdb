from elixir import Field
from elixir import String, Integer, Boolean, Enum
from elixir import using_options, has_many

from .base import Base


class PackageLocations(Base):
    using_options(tablename='package_locations')

    id = Field(Integer, colname='pkgLocationID', primary_key=True)
    pkg_type = Field(String(length=255), nullable=False)
    pkg_name = Field(String(length=255), nullable=False, unique=True)
    app_name = Field(String(length=255), nullable=False, unique=True)
    path = Field(String(length=255), nullable=False, unique=True)
    build_host = Field(String(length=30), nullable=False)
    environment = Field(Boolean, nullable=False)

    arch = Field(
        String(length=6),
        Enum(u'i386', u'x86_64', u'noarch'),
        nullable=False,
        default='noarch',
        server_default='noarch'
    )
    project_type = Field(
        String(length=12),
        Enum(u'application', u'kafka-config', u'tagconfig'),
        nullable=False,
        default='application',
        server_default='application'
    )

    # TODO: should this be has_one?
    # has_many(
    #     'app_packages',
    #     of_kind='AppPackages',
    #     colname='pkgLocationID'
    # )
    # has_many(
    #     'app_definitions',
    #     of_kind='AppDefinitions',
    #     through='app_package',
    #     via='app_definition'
    # )
    # has_many('deployments', of_kind='Deployments', colname='package_id')
