from elixir import Field
from elixir import String, Integer, Enum, DateTime
from elixir import using_options, belongs_to
from sqlalchemy.sql.expression import func

from .base import Base


class Deployments(Base):
    using_options(tablename='deployments')

    id = Field(Integer, colname='DeploymentID', primary_key=True)
    user = Field(String(length=32), nullable=False)
    dep_type = Field(
        Enum('deploy', 'rollback'),
        nullable=False,
    )

    declared = Field(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
    )

    belongs_to(
        'package',
        of_kind='Packages',
        colname='package_id',
        target_column='package_id',
        inverse='deployments'
    )
