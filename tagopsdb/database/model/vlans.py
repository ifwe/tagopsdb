from sqlalchemy import Column, ForeignKey, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base

from .environments import Environments


class Vlans(Base):
    __tablename__ = 'vlans'

    id = Column(u'VlanID', INTEGER(), primary_key=True)
    name = Column(VARCHAR(length=20))
    environment_id = Column(u'environmentID', INTEGER(),
                            ForeignKey(Environments.id, ondelete='cascade'))
    description = Column(VARCHAR(length=50))

    subnets = relationship('Subnet')

    def __init__(self, name, description):
        """ """

        self.name = name
        self.description = description
