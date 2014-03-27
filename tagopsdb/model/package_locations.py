from elixir import Field
from elixir import String, Integer, Boolean, Enum
from elixir import using_options, has_and_belongs_to_many

from .base import Base


class PackageLocations(Base):
    using_options(tablename='package_locations')

    id = Field(Integer, colname='pkgLocationID', primary_key=True)
    pkg_type = Field(String(length=255), required=True)
    name = Field(
        String(length=255),
        colname='pkg_name',
        required=True,
        unique=True
    )
    app_name = Field(String(length=255), required=True, unique=True)
    path = Field(String(length=255), required=True, unique=True)
    build_host = Field(String(length=30), required=True)
    environment = Field(Boolean, required=True)

    arch = Field(
        String(length=6),
        Enum(u'i386', u'x86_64', u'noarch'),
        required=True,
        default='noarch',
        server_default='noarch'
    )
    project_type = Field(
        String(length=12),
        Enum(u'application', u'kafka-config', u'tagconfig'),
        required=True,
        default='application',
        server_default='application'
    )

    has_and_belongs_to_many(
        'apps',
        of_kind='Application',
        inverse='package_locations',
        tablename='app_packages',
        local_colname='pkgLocationID',
        remote_colname='AppID',
        table_kwargs=dict(extend_existing=True),
    )

    # TODO: should this be has_one?
    # has_many(
    #     'app_packages',
    #     of_kind='AppPackage',
    #     colname='pkgLocationID'
    # )
    # has_many(
    #     'app_definitions',
    #     of_kind='Application',
    #     through='app_package',
    #     via='app_definition'
    # )
    # has_many('deployments', of_kind='Deployment', colname='package_id')
