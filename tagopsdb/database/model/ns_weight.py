from elixir import Field
from elixir import Integer
from elixir import using_options, belongs_to
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import TINYINT

from .base import Base


class NsWeight(Base):
    using_options(tablename='ns_weight')

    vip_id = Field(
        Integer,
        ForeignKey('ns_vip.vipID'),
        colname='vipID',
        primary_key=True
    )
    # spec_id = Field(Integer, colname='specID', primary_key=True)
    weight = Field(TINYINT(display_width=3, unsigned=True), nullable=False)

    belongs_to('ns_vip', of_kind='NsVip', field=vip_id)
    # belongs_to('host_spec', of_kind='HostSpecs', colname='specID', primary_key=True)
