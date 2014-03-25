from .base import Base
from elixir import using_options, belongs_to


class AppJmxAttributes(Base):
    using_options(tablename='app_jmx_attributes')
    belongs_to(
        'app',
        of_kind='AppDefinitions',
        colname='AppID',
        primary_key=True
    )
    belongs_to(
        'jmx_attributes',
        of_kind='JmxAttributes',
        colname='jmx_attribute_id',
        primary_key=True
    )
