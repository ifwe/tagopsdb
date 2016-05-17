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
