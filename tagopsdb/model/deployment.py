from elixir import Field
from elixir import String, Integer, Enum
from elixir import using_options, belongs_to, has_many
from sqlalchemy.sql.expression import func
from sqlalchemy.dialects.mysql import TIMESTAMP

from .base import Base


class Deployment(Base):
    using_options(tablename='deployments')

    id = Field(Integer, colname='DeploymentID', primary_key=True)
    user = Field(String(length=32), required=True)
    dep_type = Field(
        Enum('deploy', 'rollback'),
        required=True,
    )

    declared = Field(
        TIMESTAMP,
        required=True,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
    )

    belongs_to(
        'package',
        of_kind='Package',
        colname='package_id',
        target_column='package_id',
        ondelete='cascade',
        required=True,
        inverse='deployments'
    )

    has_many(
        'app_deployments',
        of_kind='AppDeployment',
        inverse='deployment',
    )

    has_many(
        'host_deployments',
        of_kind='HostDeployment',
        inverse='deployment',
    )
