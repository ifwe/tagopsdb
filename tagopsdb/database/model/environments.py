from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base


class Environments(Base):
    __tablename__ = 'environments'

    id = Column(u'environmentID', INTEGER(), primary_key=True)
    environment = Column(VARCHAR(length=15), nullable=False, unique=True)
    env = Column(VARCHAR(length=12), nullable=False, unique=True)
    domain = Column(VARCHAR(length=32), nullable=False, unique=True)
    prefix = Column(VARCHAR(length=1), nullable=False)

    host_specs = relationship('DefaultSpecs')
    # XXX: should this be NsServices ?
    ns_services = relationship('NsVipBinds')
    ns_vips = relationship('NsVipBinds')

    def __init__(self, environment, env, domain, prefix):
        """ """

        self.environment = environment
        self.env = env
        self.domain = domain
        self.prefix = prefix
