from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import relationship

from .meta import Base, Column


class DefaultSpec(Base):
    __tablename__ = 'default_specs'

    spec_id = Column(
        u'specID',
        INTEGER(),
        ForeignKey('host_specs.specID', ondelete='cascade'),
        primary_key=True
    )
    app_id = Column(
        u'AppID',
        SMALLINT(display_width=6),
        ForeignKey('app_definitions.AppID', ondelete='cascade'),
        primary_key=True
    )
    environment_id = Column(
        u'environmentID',
        INTEGER(),
        ForeignKey('environments.environmentID', ondelete='cascade'),
        primary_key=True
    )
    priority = Column(
        INTEGER(display_width=4),
        nullable=False,
        server_default='10'
    )
    host_spec = relationship('HostSpec', uselist=False)
