from .base import Base
from elixir import using_options, belongs_to


class AppHipchatRooms(Base):
    using_options(tablename='app_hipchat_rooms')
    belongs_to('app', of_kind='AppDefinitions', colname='AppID', primary_key=True)
    belongs_to('hipchat_room', of_kind='Hipchat', colname='roomID', primary_key=True)
