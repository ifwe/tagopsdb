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

import sqlalchemy.orm.exc

from sqlalchemy import func
from sqlalchemy.sql import and_

import tagopsdb.deploy.repo as repo

from tagopsdb import Session
from tagopsdb.model import AppDefinition, AppDeployment, \
    Deployment, Environment, Hipchat, HostDeployment, Host, Package, \
    PackageDefinition
from tagopsdb.exceptions import DeployException


def _calculate_environment_id(environment):
    """"""

    return (Session.query(Environment.id)
                   .filter_by(environment=environment)
                   .one())[0]


def add_deployment(user):
    """Add deployment for a given package ID"""

    dep = Deployment(
        user=user,
        # THIS NEEDS TO BE REMOVED ONCE THE NEW DEPLOY CODE
        # IS IN PLACE - KEL 20150827
        status='complete',
        declared=func.current_timestamp()
    )

    # Commit to DB immediately
    Session.add(dep)
    Session.commit()

    Session.flush()   # Needed to get DeploymentID generated

    return dep


def add_app_deployment(dep_id, app_id, user, status, environment, package_id):
    """Add a tier deployment for a given deployment ID"""

    environment_id = _calculate_environment_id(environment)

    app_dep = AppDeployment(
        deployment_id=dep_id,
        app_id=app_id,
        user=user,
        status=status,
        environment_id=environment_id,
        realized=func.current_timestamp(),
        package_id=package_id,
    )

    # Commit to DB immediately
    Session.add(app_dep)
    Session.commit()

    return app_dep


def add_host_deployment(dep_id, host_id, user, status, package_id):
    """Add host deployment for a given host and deployment"""

    host_dep = HostDeployment(
        deployment_id=dep_id,
        host_id=host_id,
        user=user,
        status=status,
        realized=func.current_timestamp(),
        package_id=package_id,
    )

    # Commit to DB immediately
    Session.add(host_dep)
    Session.commit()

    return host_dep


def delete_host_deployment(hostname, package_name):
    """ """

    host_deps = (Session.query(HostDeployment)
                 .join(Host)
                 .join(Package)
                 .filter(Package.pkg_name == package_name)
                 .filter(Host.hostname == hostname)
                 .all())

    # Allow this to silently do nothing if there are no matching rows
    for host_dep in host_deps:
        # Commit to DB immediately
        Session.delete(host_dep)
        Session.commit()


def delete_host_deployments(package_name, app_id, environment):
    """ """

    host_deps = (Session.query(HostDeployment)
                 .join(Host)
                 .join(Package)
                 .filter(Package.pkg_name == package_name)
                 .filter(Host.app_id == app_id)
                 .filter(Host.environment == environment)
                 .all())

    for host_dep in host_deps:
        # Commit to DB immediately
        Session.delete(host_dep)
        Session.commit()


def find_all_app_deployments_by_apptype(package_name, apptype, environment):
    """Find all tier deployments for a given application type
       and specific environment
    """

    return (Session.query(AppDeployment)
            .join(Package)
            .join(AppDefinition)
            .filter(Package.pkg_name == package_name)
            .filter(AppDefinition.app_type == apptype)
            .filter(AppDeployment.environment == environment)
            .all())


def find_app_by_apptype(apptype):
    """Find a given application by app type"""

    try:
        return (Session.query(AppDefinition)
                .filter_by(app_type=apptype)
                .one())
    except sqlalchemy.orm.exc.NoResultFound:
        return None


def find_apptype_by_appid(app_id):
    """Find the app type for a given ID"""

    try:
        app_def = (Session.query(AppDefinition)
                   .filter_by(id=app_id)
                   .one())
        return app_def.app_type
    except sqlalchemy.orm.exc.NoResultFound:
        raise DeployException('No app type with AppID "%s" was found '
                              'in the app_definitions table' % app_id)


def find_deployment_by_id(dep_id):
    """Find deployment for a given ID"""

    try:
        return (Session.query(Deployment)
                .filter_by(id=dep_id)
                .one())
    except sqlalchemy.orm.exc.NoResultFound:
        raise DeployException('No deployment with deploy ID "%s" found '
                              'in the deployments table' % dep_id)


def find_host_by_hostname(hostname):
    """Find host for a given hostname"""

    try:
        return (Session.query(Host)
                       .filter_by(hostname=hostname)
                       .one())
    except sqlalchemy.orm.exc.NoResultFound:
        raise DeployException('No host with hostname "%s" found in '
                              'the hosts table' % hostname)


def find_host_deployment_by_depid(dep_id, dep_host):
    """Find host deployment (if exists) for a given deployment ID"""

    try:
        return (Session.query(HostDeployment)
                       .join(Host)
                       .filter(HostDeployment.deployment_id==dep_id)
                       .filter(Host.hostname==dep_host)
                       .one())
    except sqlalchemy.orm.exc.NoResultFound:
        # Currently this shouldn't be a fatal error
        return None


def find_host_deployments_by_pkgid(pkg_id, dep_hosts):
    """Find host deployments for a given package ID and a given
       set of hosts
    """

    return (Session.query(HostDeployment, Host.hostname, Host.app_id)
                .join(Host)
                .join(Package)
                .filter(Package.id==pkg_id)
                .filter(Host.hostname.in_(dep_hosts))
                .all())


def find_host_deployments_by_package_name(package_name, dep_hosts):
    """Find host deployments for a given package and a given
       set of hosts
    """

    return (Session.query(HostDeployment, Host.hostname, Host.app_id,
                          Package.version)
                   .join(Host)
                   .join(Package)
                   .filter(Package.pkg_name==package_name)
                   .filter(Host.hostname.in_(dep_hosts))
                   .all())


def find_host_deployments_not_ok(pkg_id, app_id, environment):
    """Find host deployments that are not in 'ok' state for a given
       package ID, app ID and environment (may return none)
    """

    return (Session.query(HostDeployment, Host.hostname)
                   .join(Host)
                   .filter(HostDeployment.package_id==pkg_id)
                   .filter(Host.app_id==app_id)
                   .filter(Host.environment==environment)
                   .filter(HostDeployment.status!='ok')
                   .all())


def find_hosts_for_app(app_id, environment):
    """Find the hosts for a given application and environment"""

    return (Session.query(Host)
                    .join(AppDefinition)
                    .filter(AppDefinition.id==app_id)
                    .filter(Host.environment==environment)
                    .all())


def find_hipchat_rooms_for_app(project, apptypes=None):
    """Find the relevent HipChat rooms (if any) for a given project"""

    app_defs = repo.find_app_packages_mapping(project)

    if apptypes is None:
        proj_type = repo.find_project_type(project)[0]

        # If project isn't an application, don't add any rooms
        # (since it will add _all_ rooms the config project is
        # valid for, which would be wrong)
        if proj_type != 'application':
            return []

        apptypes = [ x.app_type for x in app_defs ]

    rooms_query = (Session.query(Hipchat.room_name)
                          .filter(Hipchat.app_definitions.any(
                                  AppDefinition.app_type.in_(apptypes)))
                          .all())

    return [ x[0] for x in rooms_query ]


def find_latest_deployment(package_name, app_id, environment):
    """Find the most recent deployment for a given package in a given
       environment for the given application ID
    """

    return (Session.query(AppDeployment, Package)
                   .join(Package)
                   .filter(Package.pkg_name==package_name)
                   .filter(AppDeployment.app_id==app_id)
                   .filter(AppDeployment.environment==environment)
                   .filter(AppDeployment.status!='invalidated')
                   .order_by(AppDeployment.realized.desc(), AppDeployment.id.desc())
                   .first())


def find_latest_validated_deployment(package_name, app_id, environment):
    """Find the most recent deployment that was validated for a given
       package, application type and environment.
    """

    return (Session.query(AppDeployment, Package.id)
                   .join(Package)
                   .filter(Package.pkg_name==package_name)
                   .filter(AppDeployment.environment==environment)
                   .filter(AppDeployment.status=='validated')
                   .order_by(AppDeployment.realized.desc(), AppDeployment.id.desc())
                   .first())


def find_previous_validated_deployment(package_name, app_id, environment):
    """Find the previous validated deployment, ignoring if the current
       deployment is validated or not, for a given package, application
       type and environment.
    """

    # Get current deployment
    app_dep, pkg = find_latest_deployment(package_name, app_id, environment)

    return (Session.query(AppDeployment, Package.id)
                   .join(Package)
                   .filter(AppDeployment.id!=app_dep.id)
                   .filter(Package.pkg_name==package_name)
                   .filter(AppDeployment.app_id==app_id)
                   .filter(AppDeployment.environment==environment)
                   .filter(AppDeployment.status=='validated')
                   .order_by(AppDeployment.realized.desc(), AppDeployment.id.desc())
                   .first())


def find_running_deployment(app_id, environment, hosts=None):
    """Find a currently running tier or host deployment (or deployments)
       for a given application type and environment
    """

    tier = (Session.query(AppDeployment.user, AppDeployment.realized,
                          AppDeployment.environment,
                          AppDefinition.app_type)
                   .join(AppDefinition)
                   .filter(AppDeployment.app_id==app_id)
                   .filter(AppDeployment.environment==environment)
                   .filter(AppDeployment.status=='inprogress')
                   .order_by(AppDeployment.realized.desc(), AppDeployment.id.desc())
                   .first())

    if tier:
        return ('tier', tier)

    host = (Session.query(HostDeployment.user, HostDeployment.realized,
                          Host.hostname, Host.environment)
                   .join(Host)
                   .filter(Host.environment==environment)
                   .filter(Host.app_id==app_id)
                   .filter(HostDeployment.status=='inprogress')
                   .all())

    if host:
        return ('host', host)

    # Get here then nothing to return
    return None


def find_unvalidated_deployments(environment):
    """ Within the given environment, find deployments that are the latest and
        need to be validated.
    """
    # Make a subquery to find the latest non-invalidated deployments of every
    # package on every appType in the specified environment, as long as there
    # is a host of that appType in the specified environment.
    latest = Session.query(
        AppDeployment.app_id.label('app_id'),
        Environment.id.label('environment_id'),
        Package.pkg_def_id.label('pkg_def_id'),
        func.max(AppDeployment.realized).label('realized'),
    ).join(
        Environment,
    ).join(
        Package,
    ).join(
        Host,
        and_(
            Environment.id == Host.environment_id,
            AppDeployment.app_id == Host.app_id,
        ),
    ).filter(
        Environment.environment == environment,
        AppDeployment.status != 'invalidated',
    ).group_by(
        AppDeployment.app_id,
        Environment.id,
        Package.pkg_def_id,
    ).subquery(
        name='t_latest',
    )

    # Return information about the deployments found in the subquery.
    non_validated = Session.query(
        AppDeployment,
    ).join(
        Environment,
    ).join(
        Package,
    ).join(
        AppDefinition,
    ).join(
        latest,
        and_(
            # Join on every item of uniqueness from the subquery.
            # AppDeployment.realized is a unique key and the rest are primary
            # keys.
            latest.c.app_id == AppDeployment.app_id,
            latest.c.realized == AppDeployment.realized,
            latest.c.environment_id == AppDeployment.environment_id,
            latest.c.pkg_def_id == Package.pkg_def_id,
        ),
    ).filter(
        Environment.environment == environment,
        AppDeployment.status.like('%complete'),
    )

    return non_validated.all()


def list_app_deployment_info(package_name, environment, name, version, revision):
    """Give all deployment information for a given package and version
       deployed to a given application tier and environment
    """

    return (Session.query(Deployment, AppDeployment, Package)
                   .join(Package)
                   .join(AppDeployment)
                   .join(AppDefinition)
                   .filter(Package.pkg_name==package_name)
                   .filter(Package.version==version)
                   .filter(Package.revision==revision)
                   .filter(AppDefinition.app_type == name)
                   .filter(AppDeployment.environment == environment)
                   .order_by(AppDeployment.realized.desc(), AppDeployment.id.desc())
                   .first())


def list_host_deployment_info(package_name, environment, version=None,
                              revision=None, apptypes=None):
    """Give all deployment information for a given package
       deployed to hosts for given (or all) application types
       and in given environment
    """

    dep_info = (Session.query(Deployment, HostDeployment, Host.hostname,
                Package)
                .join(Package)
                .join(HostDeployment)
                .join(Host)
                .join(AppDefinition))

    if version is not None:
        dep_info = dep_info.filter(Package.version == version)

    if revision is not None:
        dep_info = dep_info.filter(Package.revision == revision)

    if apptypes is not None:
        dep_info = dep_info.filter(AppDefinition.app_type.in_(apptypes))

    return (dep_info.filter(Package.pkg_name == package_name)
                    .filter(Host.environment == environment)
                    .order_by(Host.hostname,
                              HostDeployment.realized.asc())
                    .all())


def find_specific_app_deployment(package_name, environment, apptype,
                                 version=None):
    """Temporary workaround method for 'show' command to find a specific
       deployment on a given tier.
    """

    app_dep = (
        Session.query(AppDeployment)
            .join(Package)
            .join(PackageDefinition)
            .filter(PackageDefinition.name == package_name)
            .filter(AppDeployment.environment == environment)
            .filter(AppDeployment.status != 'invalidated')
            .filter(AppDeployment.app_id == apptype.id)
    )

    if version is not None:
        app_dep = app_dep.filter(Package.version == version)

    return app_dep.order_by(AppDeployment.id.desc()).first()


def find_current_app_deployment(package_name, environment, apptype):
    """Temporary workaround method for 'show' command to find the current
       deployment on a given tier.
    """

    return find_specific_app_deployment(package_name, environment, apptype)


def find_previous_app_deployment(package_name, environment, apptype):
    """Temporary workaround method for 'show' command to find the previous
       validated deployment on a given tier (ignoring the current deployment,
       validated or not).
    """

    # Get current deployment
    app_dep = find_current_app_deployment(package_name, environment, apptype)

    if app_dep is None:
        return None

    return (
        Session.query(AppDeployment)
            .join(Package)
            .join(PackageDefinition)
            .filter(PackageDefinition.name == package_name)
            .filter(AppDeployment.environment == environment)
            .filter(AppDeployment.status == 'validated')
            .filter(AppDeployment.app_id == apptype.id)
            .filter(AppDeployment.id != app_dep.id)
            .order_by(AppDeployment.id.desc())
            .first()
    )


def find_current_host_deployments(package_name, environment, apptype,
                                  version=None):
    """Temporary workaround method for 'show' command to find the current
       host deployments for a given tier.
    """

    # NOTE: unable to easily join PackageDefinition in here,
    # so the filtering on the package name will fail once
    # some upcoming DB schema changes are made; this will
    # need to be fixed or replaced
    host_deps = (
        Session.query(HostDeployment)
            .join(Package)
            .join(HostDeployment)
            .join(Host)
            .join(AppDefinition)
            .filter(Package.pkg_name == package_name)
            .filter(Host.environment == environment)
            .filter(AppDefinition.id == apptype.id)
    )

    if version is not None:
        host_deps = host_deps.filter(Package.version == version)

    return (
        host_deps.order_by(Host.hostname, HostDeployment.realized.asc()).all()
    )
