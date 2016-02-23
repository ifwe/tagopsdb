from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from .meta import Base, Column, String


class NetDefaultMap(Base):
    __tablename__ = 'net_default_maps'

    id = Column(u'net_default_id', INTEGER(unsigned=True), primary_key=True)
    dc_id = Column(
        INTEGER(),
        ForeignKey('datacenters.dc_id', ondelete='cascade'),
        server_default='1'
    )
    environment_id = Column(
        INTEGER(),
        ForeignKey('environments.environmentID', ondelete='cascade'),
        nullable=False
    )
    app_id = Column(
        SMALLINT(),
        ForeignKey('app_definitions.AppID', ondelete='cascade'),
        nullable=False
    )
    interface_name = Column(String(length=10), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            u'environment_id',
            u'app_id',
            u'interface_name',
            name='map_key'
        ),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
