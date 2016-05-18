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

"""update app and host deployment tables state column

Revision ID: 263eeebd28b9
Revises: 12300441b36c
Create Date: 2015-09-03 14:45:11.463435

"""

# revision identifiers, used by Alembic.
revision = '263eeebd28b9'
down_revision = '12300441b36c'

from alembic import op
import sqlalchemy as sa


app_new_type = sa.Enum(
    u'complete',
    u'incomplete',
    u'inprogress',
    u'invalidated',
    u'pending',
    u'validated',
)
app_old_type = sa.Enum(
    u'complete',
    u'incomplete',
    u'inprogress',
    u'invalidated',
    u'validated',
)
host_new_type = sa.Enum(
    u'failed',
    u'inprogress',
    u'ok',
    u'pending',
)
host_old_type = sa.Enum(
    u'inprogress',
    u'failed',
    u'ok',
)


def upgrade():
    op.alter_column(
        'app_deployments',
        'status',
        nullable=False,
        type_=app_new_type,
        existing_type=app_old_type
    )
    op.alter_column(
        'host_deployments',
        'status',
        nullable=False,
        type_=host_new_type,
        existing_type=host_old_type
    )


def downgrade():
    op.alter_column(
        'app_deployments',
        'status',
        nullable=False,
        type_=app_old_type,
        existing_type=app_new_type
    )
    op.alter_column(
        'host_deployments',
        'status',
        nullable=False,
        type_=host_old_type,
        existing_type=host_new_type
    )
