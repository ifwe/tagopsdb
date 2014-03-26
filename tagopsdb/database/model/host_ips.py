from elixir import Field
from elixir import String, Integer
from elixir import using_options, belongs_to, has_many

from .base import Base


class HostIps(Base):
    using_options(tablename='host_ips')

    id = Field(Integer, colname='IpID', primary_key=True)
    priority = Field(Integer, required=True, default=1, server_default='1')
    a_record = Field(String(length=200), colname='ARecord')
    comments = Field(String(length=200))

    belongs_to(
        'interface',
        of_kind='HostInterfaces',
        colname='InterfaceID',
        ondelete='cascade',
        required=True,
    )

    belongs_to(
        'subnet',
        of_kind='Subnet',
        colname='SubnetID',
        ondelete='cascade',
        required=True,
    )

    has_many(
        'cnames',
        of_kind='Cname',
        inverse='host_ip',
    )
