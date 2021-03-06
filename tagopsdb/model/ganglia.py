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

from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Ganglia(Base):
    __tablename__ = 'ganglia'

    id = Column(u'GangliaID', INTEGER(), primary_key=True)
    cluster_name = Column(String(length=50))
    port = Column(
        INTEGER(display_width=5),
        nullable=False,
        server_default='8649'
    )
    app_definitions = relationship('AppDefinition')
