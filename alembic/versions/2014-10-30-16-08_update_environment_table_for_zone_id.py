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
