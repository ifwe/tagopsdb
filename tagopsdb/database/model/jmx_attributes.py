from elixir import Field
from elixir import Integer, String
from elixir import using_options

from .base import Base


class JmxAttributes(Base):
    using_options(tablename='jmx_attributes')

    id = Field(Integer, colname='jmx_attribute_id', primary_key=True)
    obj = Field(String(length=300), required=True)
    attr = Field(String(length=300), required=True)
    ganglia_group_name = Field(String(length=25), colname='GgroupName')
