from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class VmInfo(Base):
    __tablename__ = 'vm_info'

    host_id = Column(
        u'host_id',
        INTEGER(),
        ForeignKey(
            'hosts.HostID',
            name='fk_vm_info_host_id_hosts',
            ondelete='cascade'
        ),
        primary_key=True
    )
    pool = Column(String(length=10), nullable=False)
    numa_mode = Column(INTEGER(), server_default=None)

    host = relationship('Host', uselist=False)
