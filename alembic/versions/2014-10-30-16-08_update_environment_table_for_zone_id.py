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

"""update environment table for zone id

Revision ID: 46d842a18450
Revises: 2dc22680b176
Create Date: 2014-10-30 16:08:01.084752

"""

# revision identifiers, used by Alembic.
revision = '46d842a18450'
down_revision = '2dc22680b176'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import INTEGER


def upgrade():
    op.add_column(
        'environments',
        sa.Column(
            'zone_id',
            INTEGER(),
            info={'after': 'prefix'}
        )
    )
    op.execute(
        'update environments join zones on environments.domain = '
        'zones.zoneName set environments.zone_id = zones.ZoneID'
    )
    op.alter_column(
        'environments',
        'zone_id',
        nullable=False,
        existing_type=INTEGER()
    )
    op.create_foreign_key(
        'fk_environments_zone_id_zones',
        'environments',
        'zones',
        ['zone_id'],
        ['zoneID']
    )


def downgrade():
    op.drop_constraint(
        'fk_environments_zone_id_zones',
        'environments',
        type_='foreignkey'
    )
    op.drop_column('environments', 'zone_id')
