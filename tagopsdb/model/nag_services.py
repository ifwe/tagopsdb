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

from .meta import Base, Column, String, SurrogatePK


class NagService(SurrogatePK, Base):
    __tablename__ = 'nag_services'

    check_command_id = Column(
        INTEGER(),
        ForeignKey('nag_check_commands.id', ondelete='cascade'),
        nullable=False
    )
    description = Column(String(length=255), nullable=False)
    max_check_attempts = Column(INTEGER(), nullable=False)
    check_interval = Column(INTEGER(), nullable=False)
    check_period_id = Column(
        INTEGER(),
        ForeignKey('nag_time_periods.id', ondelete='cascade'),
        nullable=False
    )
    retry_interval = Column(INTEGER(), nullable=False)
    notification_interval = Column(INTEGER(), nullable=False)
    notification_period_id = Column(
        INTEGER(),
        ForeignKey('nag_time_periods.id', ondelete='cascade'),
        nullable=False
    )
    applications = relationship('NagApptypesServices')
    check_period = relationship(
        'NagTimePeriod',
        foreign_keys=[ check_period_id ],
        uselist=False
    )
    command_arguments = relationship(
        'NagServicesArguments',
        backref='nag_services'
    )
    contact_groups = relationship(
        'NagContactGroup',
        secondary='nag_services_contact_groups',
        backref='nag_services'
    )
    contacts = relationship(
        'NagContact',
        secondary='nag_services_contacts',
        backref='nag_services'
    )
    environments = relationship('NagApptypesServices')
    hosts = relationship('NagHostsServices')
    nag_check_command = relationship(
        'NagCheckCommand',
        uselist=False,
        backref='nag_services'
    )
    notification_period = relationship(
        'NagTimePeriod',
        foreign_keys=[ notification_period_id ],
        uselist=False
    )
