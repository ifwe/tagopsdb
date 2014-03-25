from elixir import Field
from elixir import String, Integer, Enum, DateTime
from elixir import using_options, belongs_to
from sqlalchemy.sql.expression import func

from .base import Base


class AppDeployments(Base):
    using_options(tablename='app_deployments')

    id = Field(Integer, colname='AppDeploymentID', primary_key=True)
    user = Field(String(length=32), nullable=False)
    status = Field(
        Enum(
            'complete',
            'incomplete',
            'inprogress',
            'invalidated',
            'validated'
        ),
        nullable=False
    )
    environment = Field(String(length=15), nullable=False)

    realized = Field(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
    )

    belongs_to('deployment', of_kind='Deployments', colname='DeploymentID')
    belongs_to('app', of_kind='AppDefinitions', colname='AppID')
