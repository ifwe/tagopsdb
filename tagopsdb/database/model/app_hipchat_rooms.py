from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from .base import Base

from .hipchat import Hipchat


AppHipchatRooms = app_hipchat_rooms = Table(
    u'app_hipchat_rooms',
    Base.metadata,
    Column(u'AppID', SMALLINT(display_width=6),
           ForeignKey('app_definitions.AppID', ondelete='cascade'),
           primary_key=True),
    Column(u'roomID', INTEGER(), ForeignKey(Hipchat.id, ondelete='cascade'),
           primary_key=True),
    mysql_engine='InnoDB', mysql_charset='utf8',
)
