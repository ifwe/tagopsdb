from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from sqlalchemy.orm import relationship

from .base import Base


class DefaultSpecs(Base):
    __tablename__ = 'default_specs'

    spec_id = Column(u'specID', INTEGER(),
                     ForeignKey('host_specs.specID', ondelete='cascade'),
                     primary_key=True)
    app_id = Column(u'AppID', SMALLINT(display_width=6),
                    ForeignKey('app_definitions.AppID', ondelete='cascade'),
                    primary_key=True)
    environment_id = Column(
        u'environmentID',
        INTEGER(),
        ForeignKey('environments.environmentID', ondelete='cascade'),
        primary_key=True
    )
    priority = Column(INTEGER(display_width=4), nullable=False, default='10',
                      server_default='10')

    host_spec = relationship('HostSpecs', uselist=False)

    def __init__(self, spec_id, app_id, environment_id, priority):
        """ """

        self.spec_id = spec_id
        self.app_id = app_id
        self.environment_id = environment_id
        self.priority = priority
