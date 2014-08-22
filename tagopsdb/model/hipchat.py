from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from .meta import Base, Column, String


class Hipchat(Base):
    __tablename__ = 'hipchat'

    id = Column(u'roomID', INTEGER(), primary_key=True)
    room_name = Column(String(length=50), nullable=False, unique=True)
    app_definitions = relationship(
        'AppDefinition',
        secondary='app_hipchat_rooms',
        back_populates='hipchats'
    )
