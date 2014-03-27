from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base


class Hipchat(Base):
    __tablename__ = 'hipchat'

    id = Column(u'roomID', INTEGER(), primary_key=True)
    room_name = Column(VARCHAR(length=50), nullable=False, unique=True)

    def __init__(self, room_name):
        """ """

        self.room_name = room_name
