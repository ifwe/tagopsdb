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

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER

from .meta import Base, Column, String, SurrogatePK


class NagCommandArgument(SurrogatePK, Base):
    __tablename__ = 'nag_command_arguments'

    check_command_id = Column(
        INTEGER(),
        ForeignKey('nag_check_commands.id', ondelete='cascade'),
        nullable=False
    )
    label = Column(String(length=32), nullable=False)
    description = Column(String(length=255), nullable=False)
    arg_order = Column(INTEGER(), nullable=False)
    default_value = Column(String(length=80))

    __table_args__ = (
        UniqueConstraint(u'check_command_id', u'arg_order',
                         name='check_command_arg_order'),
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )
