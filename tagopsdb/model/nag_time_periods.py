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

from .meta import Base, Column, String, SurrogatePK


class NagTimePeriod(SurrogatePK, Base):
    __tablename__ = 'nag_time_periods'

    name = Column(String(length=32), nullable=False, unique=True)
    alias = Column(String(length=80))
    sunday = Column(String(length=32))
    monday = Column(String(length=32))
    tuesday = Column(String(length=32))
    wednesday = Column(String(length=32))
    thursday = Column(String(length=32))
    friday = Column(String(length=32))
    saturday = Column(String(length=32))
