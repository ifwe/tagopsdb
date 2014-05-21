import sqlalchemy.orm.exc

from sqlalchemy import func
from sqlalchemy.sql import and_

import tagopsdb.deploy.repo as repo

from tagopsdb.model import Session
from tagopsdb.model import AppDefinition, AppDeployment, \
    Deployment, Hipchat, HostDeployment, Host, Package
from tagopsdb.exceptions import DeployException


def add_deployment(pkg_id, user, dep_type):
    """Add deployment for a given package ID"""

    dep = Deployment(
        package_id=pkg_id,
        user=user,
        dep_type=dep_type,
        declared=func.current_timestamp()
    )

    # Commit to DB immediately
    Session.add(dep)
    Session.commit()

    Session.flush()   # Needed to get DeploymentID generated

    return dep


def add_app_deployment(dep_id, app_id, user, status, environment):
    """Add a tier deployment for a given deployment ID"""

    app_dep = AppDeployment(
        deployment_id=dep_id,
        app_id=app_id,
        user=user,
        status=status,
        environment=environment,
        realized=func.current_timestamp()
    )

    # Commit to DB immediately
    Session.add(app_dep)
    Session.commit()

    return app_dep


def add_host_deployment(dep_id, host_id, user, status):
    """Add host deployment for a given host and deployment"""

    host_dep = HostDeployment(
        deployment_id=dep_id,
        host_id=host_id,
        user=user,
        status=status,
        realized=func.current_timestamp()
    )

    # Commit to DB immediately
    Session.add(host_dep)
    Session.commit()

    return host_dep


def delete_host_deployment(hostname, package_name):
    """ """

    host_deps = (Session.query(HostDeployment)
                 .join(Host)
                 .join(Deployment)
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
                 .join(Deployment)
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
            .join(Deployment)
            .join(Package)
            .join(AppDefinition)
            .filter(Package.pkg_name == package_name)
            .filter(AppDefinition.app_type == apptype)
            .filter(AppDeployment.environment == environment)
            .all())


def find_app_deployment(pkg_id, app_ids, environment):
    """Find specific tier deployment(s) based on package ID and
       application ID(s)
    """

    subq = (Session.query(AppDeployment.app_id, AppDefinition.app_type,
            AppDeployment.id, Deployment.dep_type)
            .join(Deployment)
            .join(Package)
            .join(AppDefinition)
            .filter(Package.id == pkg_id)
            .filter(AppDeployment.app_id.in_(app_ids))
            .filter(AppDeployment.environment == environment)
            .order_by(AppDeployment.realized.desc())
            .subquery(name='t_ordered'))

    return (Session.query(AppDeployment, AppDefinition.app_type,
            Deployment.dep_type, Package)
            .join(AppDefinition)
            .join(Deployment)
            .join(Package)
            .join(subq, AppDeployment.id == subq.c.AppDeploymentID)
            .group_by(subq.c.AppID)
            .all())


def find_app_by_apptype(apptype):
    """Find a given application by app type"""

    try:
        return (Session.query(AppDefinition)
                .filter_by(app_type=apptype)
                .one())
    except sqlalchemy.orm.exc.NoResultFound:
        raise DeployException('App type "%s" not found in the '
                              'app_definitions table' % apptype)


def find_app_by_depid(dep_id):
    """Find a given application and version by deployment ID"""

    try:
        return (Session.query(Package)
                .join(Deployment)
                .filter(Deployment.id == dep_id)
                .one())
    except sqlalchemy.orm.exc.NoResultFound:
        raise DeployException('No deployment with deploy ID "%s" found '
                              'in the deployments table' % dep_id)


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


def find_deployed_version(package_name, env, version=None, revision=None,
                          apptypes=None, apptier=False):
    """Find a given deployed version for a given package in a given
       environment for all related app types; search for full tier
       or host only deployment specifically
    """

    if apptier:
        subq = (
            Session.query(
                Package.pkg_name,
                Package.version,
                Package.revision,
                AppDefinition.app_type,
                AppDeployment.environment
            ).join(Deployment)
             .join(AppDeployment)
             .join(AppDefinition)
             .filter(Package.pkg_name == package_name)
             .filter(AppDeployment.environment == env)
             .filter(AppDeployment.status != 'invalidated'))

        if apptypes is not None:
            subq = subq.filter(AppDefinition.app_type.in_(apptypes))

        if version is not None:
            subq = subq.filter(Package.version == version)

        if revision is not None:
            subq = subq.filter(Package.revision == revision)

        subq = (subq.order_by(AppDeployment.realized.desc())
                    .subquery(name='t_ordered'))

        # The actual column name must be used in the subquery
        # usage below; DB itself should be corrected
        versions = (Session.query(subq.c.appType,
                    subq.c.version,
                    subq.c.revision)
                    .group_by(subq.c.appType, subq.c.environment)
                    .all())
    else:
        hostsq = (Session.query(Host.hostname, Host.app_id,
                  Package.version, Package.revision)
                  .join(AppDefinition)
                  .join(HostDeployment)
                  .join(Deployment)
                  .join(Package)
                  .filter(Package.pkg_name == package_name)
                  .filter(Host.environment == env))

        if apptypes is not None:
            hostsq = hostsq.filter(AppDefinition.app_type.in_(apptypes))

        versions = (hostsq.all())

    return versions


def find_deployment_by_id(dep_id):
    """Find deployment for a given ID"""

    try:
        return (Session.query(Deployment)
                .filter_by(id=dep_id)
                .one())
    except sqlalchemy.orm.exc.NoResultFound:
        raise DeployException('No deployment with deploy ID "%s" found '
                              'in the deployments table' % dep_id)


def find_deployment_by_pkgid(pkg_id):
    """Find deployment(s) for a given package ID"""

    return (Session.query(Deployment)
                   .filter_by(package_id=pkg_id)
                   .order_by(Deployment.declared.desc())
                   .all())


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

    return (Session.query(HostDeployment, Host.hostname, Host.app_id,
                          Deployment.dep_type)
                   .join(Host)
                   .join(Deployment)
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
                   .join(Deployment)
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
                   .join(Deployment)
                   .filter(Deployment.package_id==pkg_id)
                   .filter(Host.app_id==app_id)
                   .filter(Host.environment==environment)
                   .filter(HostDeployment.status!='ok')
                   .all())


def find_hosts_for_app(app_id, environment):
    """Find the hosts for a given application and environment"""

    hosts = (Session.query(Host)
                    .join(AppDefinition)
                    .filter(AppDefinition.id==app_id)
                    .filter(Host.environment==environment)
                    .all())

    if not hosts:
        raise DeployException('No hosts found for AppID "%s" in '
                              'environment "%s" in the database'
                              % (app_id, environment))

    return hosts


def find_hipchat_rooms_for_app(project, apptypes=None):
    """Find the relevent HipChat rooms (if any) for a given project"""

    if apptypes is None:
        proj_type = repo.find_project_type(project)[0]

        # If project isn't an application, don't add any rooms
        # (since it will add _all_ rooms the config project is
        # valid for, which would be wrong)
        if proj_type != 'application':
            return []

        app_defs = repo.find_app_packages_mapping(project)
        apptypes = [ x.app_type for x in app_defs ]

    rooms_query = (Session.query(Hipchat.room_name)
                          .filter(Hipchat.app_definitions.any(
                                  AppDefinition.app_type.in_(apptypes)))
                          .all())

    return [ x[0] for x in rooms_query ]


def find_latest_deployed_version(package_name, env, apptypes=None,
                                 apptier=False):
    """Find the most recent deployed version for a given package
       in a given environment for all related app types; search
       for full tier or host only deployment specifically
    """

    return find_deployed_version(package_name, env, apptypes=apptypes,
                                 apptier=apptier)


def find_latest_deployment(package_name, app_id, env):
    """Find the most recent deployment for a given package in a given
       environment for the given application ID
    """

    return (Session.query(AppDeployment, Package)
                   .join(Deployment)
                   .join(Package)
                   .filter(Package.pkg_name==package_name)
                   .filter(AppDeployment.app_id==app_id)
                   .filter(AppDeployment.environment==env)
                   .filter(AppDeployment.status!='invalidated')
                   .order_by(AppDeployment.realized.desc())
                   .first())


def find_latest_validated_deployment(package_name, app_id, env):
    """Find the most recent deployment that was validated for a given
       package, application type and environment.
    """

    return (Session.query(AppDeployment, Package.id)
                   .join(Deployment)
                   .join(Package)
                   .filter(Package.pkg_name==package_name)
                   .filter(AppDeployment.environment==env)
                   .filter(AppDeployment.status=='validated')
                   .order_by(AppDeployment.realized.desc())
                   .first())


def find_previous_validated_deployment(package_name, app_id, env):
    """Find the previous validated deployment, ignoring if the current
       deployment is validated or not, for a given package, application
       type and environment.
    """

    # Get current deployment
    app_dep, pkg = find_latest_deployment(package_name, app_id, env)

    return (Session.query(AppDeployment, Package.id)
                   .join(Deployment)
                   .join(Package)
                   .filter(AppDeployment.id!=app_dep.id)
                   .filter(Package.pkg_name==package_name)
                   .filter(AppDeployment.app_id==app_id)
                   .filter(AppDeployment.environment==env)
                   .filter(AppDeployment.status=='validated')
                   .order_by(AppDeployment.realized.desc())
                   .first())


def find_running_deployment(app_id, env, hosts=None):
    """Find a currently running tier or host deployment (or deployments)
       for a given application type and environment
    """

    tier = (Session.query(AppDeployment.user, AppDeployment.realized,
                          AppDeployment.environment, AppDefinition.app_type)
                   .join(AppDefinition)
                   .filter(AppDeployment.app_id==app_id)
                   .filter(AppDeployment.environment==env)
                   .filter(AppDeployment.status=='inprogress')
                   .order_by(AppDeployment.realized.desc())
                   .first())

    if tier:
        return ('tier', tier)

    host = (Session.query(HostDeployment.user, HostDeployment.realized,
                          Host.hostname, Host.environment)
                   .join(Host)
                   .filter(Host.environment==env)
                   .filter(Host.app_id==app_id)
                   .filter(HostDeployment.status=='inprogress')
                   .all())

    if host:
        return ('host', host)

    # Get here then nothing to return
    return None


def find_unvalidated_versions(time_delta, environment):
    """Find the latest deployments that are not validated in a given
       environment for a given amount of time
    """

    subq = (Session.query(Package.pkg_name, Package.version,
                          Package.revision, AppDefinition.app_type,
                          AppDeployment.environment, AppDeployment.realized,
                          AppDeployment.user, AppDeployment.status)
                   .join(Deployment)
                   .join(AppDeployment)
                   .join(AppDefinition)
                   .filter(AppDeployment.status!='invalidated')
                   .filter(AppDeployment.environment==environment)
                   .order_by(AppDeployment.realized.desc())
                   .subquery(name='t_ordered'))

    return (Session.query(subq.c.pkg_name, subq.c.version, subq.c.revision,
                          subq.c.appType, subq.c.environment,
                          subq.c.realized, subq.c.user, subq.c.status)
                   .group_by(subq.c.appType, subq.c.environment,
                             subq.c.pkg_name)
                   .having(and_(subq.c.status.like('%complete'),
                                func.unix_timestamp(subq.c.realized) <
                                func.unix_timestamp(func.now()) - time_delta))
                   .all())


def list_app_deployment_info(package_name, env, name, version, revision):
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
                   .filter(AppDeployment.environment == env)
                   .order_by(AppDeployment.realized.desc())
                   .first())


def list_host_deployment_info(package_name, env, version=None, revision=None,
                              apptypes=None):
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
                    .filter(Host.environment == env)
                    .order_by(Host.hostname,
                              HostDeployment.realized.asc())
                    .all())
