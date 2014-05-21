from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Vlan(Base):
    __tablename__ = 'vlans'

    id = Column(u'VlanID', INTEGER(), primary_key=True)
    name = Column(String(length=20))
    environment_id = Column(
        u'environmentID',
        INTEGER(),
        ForeignKey('environments.environmentID', ondelete='cascade')
    )
    description = Column(String(length=50))
    subnets = relationship('Subnet')
