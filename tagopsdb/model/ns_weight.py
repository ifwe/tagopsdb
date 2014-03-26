from elixir import Field
from elixir import using_options, belongs_to
from sqlalchemy.dialects.mysql import TINYINT

from .base import Base


class NsWeight(Base):
    using_options(tablename='ns_weight')

    weight = Field(TINYINT(display_width=3, unsigned=True), nullable=False)

    belongs_to(
        'vip',
        of_kind='NsVip',
        colname='vipID',
        primary_key=True,
        ondelete='cascade',
    )
    belongs_to(
        'host_spec',
        of_kind='HostSpecs',
        colname='specID',
        primary_key=True,
        ondelete='cascade',
    )
