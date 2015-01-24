import sys

from sqlalchemy.types import CHAR
from sqlalchemy.ext.declarative import declarative_base

from ..model.meta import init as base_init, \
    destroy as base_destroy, \
    initialized as base_initialized, TagOpsDB

from ..model.meta import String, Column


def init(url={}, module=None, **config):
    url = dict(url)
    url.setdefault('database', 'TagOpsDB_private')

    if module is None:
        module = sys.modules[__name__]

    return base_init(url=url, module=module, **config)


def destroy(module=None, **config):
    if module is None:
        module = sys.modules[__name__]

    return base_destroy(module=module, **config)


def initialized(module=None, **config):
    if module is None:
        module = sys.modules[__name__]

    return base_initialized(module=module, **config)

Base = declarative_base(cls=TagOpsDB)


class SSHHostKeys(Base):
    __tablename__ = 'ssh_host_keys'

    hostname = Column(String(30), nullable=False, primary_key=True)
    pub = Column(String(1600), server_default=None)
    sha256 = Column(CHAR(64), server_default=None)
    priv = Column(String(2000), server_default=None)
