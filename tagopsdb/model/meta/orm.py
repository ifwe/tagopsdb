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
from sqlalchemy.ext.declarative import declared_attr


def many_to_one(clsname, **kw):
    """Use an event to build a many-to-one relationship on a class.

    This makes use of the :meth:`.References._reference_table` method
    to generate a full foreign key relationship to the remote table.
    """

    @declared_attr
    def m2o(cls):
        cls._references((cls.__name__, clsname))
        return relationship(clsname, **kw)
    return m2o


def one_to_many(clsname, **kw):
    """Use an event to build a one-to-many relationship on a class.

    This makes use of the :meth:`.References._reference_table` method
    to generate a full foreign key relationship from the remote table.
    """

    @declared_attr
    def o2m(cls):
        cls._references((clsname, cls.__name__))
        return relationship(clsname, **kw)
    return o2m