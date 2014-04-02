from elixir import Field
from elixir import String, Integer, Enum, DateTime
from elixir import using_options, belongs_to
from sqlalchemy.sql.expression import func

from .base import Base


class AppDeployment(Base):
    using_options(tablename='app_deployments')

    id = Field(Integer, colname='AppDeploymentID', primary_key=True)
    user = Field(String(length=32), required=True)
    status = Field(
        Enum(
            'complete',
            'incomplete',
            'inprogress',
            'invalidated',
            'validated'
        ),
        required=True,
    )
    environment = Field(String(length=15), required=True)

    realized = Field(
        DateTime,
        required=True,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
    )

    belongs_to(
        'deployment',
        of_kind='Deployment',
        colname='DeploymentID',
        required=True
    )
    belongs_to(
        'app',
        of_kind='Application',
        colname='AppID',
        required=True
    )
