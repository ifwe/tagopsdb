from elixir import Field
from elixir import Integer, String
from elixir import using_options, has_and_belongs_to_many

from .base import Base


class Hipchat(Base):
    using_options(tablename='hipchat')

    id = Field(Integer, colname='roomID', primary_key=True)
    name = Field(String(length=50), colname='room_name', required=True, unique=True)

    has_and_belongs_to_many(
        'apps',
        of_kind='Application',
        inverse='hipchat_rooms',
        tablename='app_hipchat_rooms',
        local_colname='roomID',
        remote_colname='AppID',
        table_kwargs=dict(extend_existing=True)
    )
