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
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class NagServicesArguments(Base):
    __tablename__ = 'nag_services_arguments'

    service_id = Column(
        INTEGER(),
        ForeignKey('nag_services.id', ondelete='cascade'),
        primary_key=True
    )
    command_argument_id = Column(
        INTEGER(),
        ForeignKey('nag_command_arguments.id', ondelete='cascade'),
        primary_key=True
    )
    value = Column(String(length=120), nullable=False)
    command_argument = relationship(
        'NagCommandArgument',
        backref='nag_services_assoc'
    )
