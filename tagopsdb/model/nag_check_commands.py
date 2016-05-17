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

from sqlalchemy.orm import relationship

from .meta import Base, Column, String, SurrogatePK


class NagCheckCommand(SurrogatePK, Base):
    __tablename__ = 'nag_check_commands'

    command_name = Column(String(length=32), nullable=False, unique=True)
    command_line = Column(String(length=255), nullable=False)
    nag_command_arguments = relationship('NagCommandArgument')
