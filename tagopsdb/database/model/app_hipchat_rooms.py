from elixir import Field, Integer
from elixir import using_options, using_table_options
from .base import Base


class AppHipchatRooms(Base):
    using_options(tablename='app_hipchat_rooms')
    using_table_options(extend_existing=True)

    AppID = Field(Integer, primary_key=True)
    roomID = Field(Integer, primary_key=True)

    ## TODO: correctly define class with these relationships:
    # belongs_to(
    #     'app',
    #     of_kind='AppDefinitions',
    #     colname='AppID',
    #     primary_key=True
    # )
    # belongs_to(
    #     'hipchat_room',
    #     of_kind='Hipchat',
    #     colname='roomID',
    #     primary_key=True
    # )
