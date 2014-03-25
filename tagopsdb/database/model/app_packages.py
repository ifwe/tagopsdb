from elixir import using_options, belongs_to
from .base import Base


class AppPackages(Base):
    using_options(tablename='app_packages')
    belongs_to(
        'app',
        of_kind='AppDefinitions',
        colname='AppID',
        primary_key=True
    )
    belongs_to(
        'package_location',
        of_kind='PackageLocations',
        colname='pkgLocationID',
        primary_key=True
    )
