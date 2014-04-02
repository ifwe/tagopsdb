from elixir import Field, Integer, using_options, using_table_options
from .base import Base


class AppJmxAttribute(Base):
    using_options(tablename='app_jmx_attributes')
    using_table_options(extend_existing=True)

    AppID = Field(Integer, primary_key=True)
    jmx_attribute_id = Field(Integer, primary_key=True)

    ## TODO: correctly define class with these relationships:
    # belongs_to(
    #     'app',
    #     of_kind='Application',
    #     colname='AppID',
    #     primary_key=True
    # )
    # belongs_to(
    #     'jmx_attributes',
    #     of_kind='JmxAttribute',
    #     colname='jmx_attribute_id',
    #     primary_key=True
    # )
