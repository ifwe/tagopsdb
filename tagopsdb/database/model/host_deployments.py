from elixir import Field
from elixir import String, Integer, Enum, DateTime
from elixir import using_options, belongs_to
from sqlalchemy.sql.expression import func

from .base import Base


class HostDeployments(Base):
    using_options(tablename='host_deployments')

    id = Field(Integer, colname='HostDeploymentID', primary_key=True)
    user = Field(String(length=32), nullable=False)
    status = Field(Enum('inprogress', 'failed', 'ok'), nullable=False)
    realized = Field(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
    )

    belongs_to('host', of_kind='Hosts', colname='HostID')
    belongs_to('deployment', of_kind='Deployments', colname='DeploymentID')
