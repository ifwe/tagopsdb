# Copyright 2016 Ifwe Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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


class SSHHostKey(Base):
    __tablename__ = 'ssh_host_keys'

    hostname = Column(String(30), nullable=False, primary_key=True)
    pub = Column(String(1600), server_default=None)
    sha256 = Column(CHAR(64), server_default=None)
    priv = Column(String(2000), server_default=None)
