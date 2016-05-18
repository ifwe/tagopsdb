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

"""update hosts table appid null

Revision ID: 41c58f565378
Revises: 263eeebd28b9
Create Date: 2015-11-19 13:39:47.403047

"""

# revision identifiers, used by Alembic.
revision = '41c58f565378'
down_revision = '263eeebd28b9'

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects.mysql import SMALLINT


def upgrade():
    op.alter_column(
        'hosts',
        'AppID',
        nullable=True,
        server_default=None,
        existing_type=SMALLINT(display_width=6)
    )

def downgrade():
    op.alter_column(
        'hosts',
        'AppID',
        nullable=False,
        existing_type=SMALLINT(display_width=6)
    )
