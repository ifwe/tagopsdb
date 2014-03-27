from elixir import Field, Integer, using_options, using_table_options

from .base import Base


class NagApptypesServices(Base):
    using_options(tablename='nag_apptypes_services')
    using_table_options(extend_existing=True)

    app_id = Field(Integer, primary_key=True)
    service_id = Field(Integer, primary_key=True)
    server_app_id = Field(Integer, primary_key=True)
    environment_id = Field(Integer, primary_key=True)

    ## TODO: correctly define class with these relationships:
    # belongs_to(
    #     'app',
    #     of_kind='Application',
    #     colname='app_id',
    #     primary_key=True,
    #     ondelete='cascade'
    # )
    # belongs_to(
    #     'service',
    #     of_kind='NagServices',
    #     colname='service_id',
    #     primary_key=True,
    #     ondelete='cascade'
    # )
    # belongs_to(
    #     'server_app',
    #     of_kind='Application',
    #     colname='server_app_id',
    #     primary_key=True
    # )
    # belongs_to(
    #     'environment',
    #     of_kind='Environments',
    #     colname='environment_id',
    #     primary_key=True,
    #     ondelete='cascade'
    # )
