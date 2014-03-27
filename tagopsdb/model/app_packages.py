from elixir import Field, Integer, using_options, using_table_options
from .base import Base


class AppPackage(Base):
    using_options(tablename='app_packages')
    using_table_options(extend_existing=True)

    AppID = Field(Integer, primary_key=True)
    pkgLocationID = Field(Integer, primary_key=True)

    ## TODO: correctly define class with these relationships:
    # belongs_to(
    #     'app',
    #     of_kind='Application',
    #     colname='AppID',
    #     primary_key=True
    # )
    # belongs_to(
    #     'package_location',
    #     of_kind='PackageLocations',
    #     colname='pkgLocationID',
    #     primary_key=True
    # )
