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

"""Move package_id from deployments to (host|tier)_deployments

Revision ID: 2b29596623f7
Revises: 1e725eb01a1f
Create Date: 2015-10-05 13:44:11.645008

"""

# revision identifiers, used by Alembic.
revision = '2b29596623f7'
down_revision = '1e725eb01a1f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'host_deployments',
        sa.Column(
            'package_id',
            sa.Integer,
            sa.ForeignKey('packages.package_id', ondelete='cascade'),
            nullable=True,
            info={'after': 'HostID'},
        ),
    )

    op.execute(
        'update host_deployments join deployments on '
        'host_deployments.DeploymentID = deployments.DeploymentID '
        'set host_deployments.package_id = deployments.package_id'
    )

    op.alter_column(
        'host_deployments',
        'package_id',
        nullable=False,
        existing_type=sa.Integer,
    )

    op.add_column(
        'app_deployments',
        sa.Column(
            'package_id',
            sa.Integer,
            sa.ForeignKey('packages.package_id', ondelete='cascade'),
            nullable=True,
            info={'after': 'AppID'},
        ),
    )

    op.execute(
        'update app_deployments join deployments on '
        'app_deployments.DeploymentID = deployments.DeploymentID '
        'set app_deployments.package_id = deployments.package_id'
    )

    op.alter_column(
        'app_deployments',
        'package_id',
        nullable=False,
        existing_type=sa.Integer,
    )


def downgrade():
    op.drop_column('host_deployments', 'package_id')
    op.drop_column('app_deployments', 'package_id')
