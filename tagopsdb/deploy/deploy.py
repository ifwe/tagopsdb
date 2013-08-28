import sqlalchemy.orm.exc

from sqlalchemy import func
from sqlalchemy.sql import and_

import tagopsdb.deploy.repo as repo

from tagopsdb.database.meta import Session
from tagopsdb.database.model import AppDefinitions, AppDeployments, \
                                    Deployments, Hipchat, HostDeployments, \
                                    Hosts, Packages
from tagopsdb.exceptions import DeployException


def add_deployment(pkg_id, user, dep_type):
    """Add deployment for a given package ID"""

    dep = Deployments(pkg_id, user, dep_type, func.current_timestamp())

    # Commit to DB immediately
    Session.add(dep)
    Session.commit()

    Session.flush()   # Needed to get DeploymentID generated

    return dep


def add_app_deployment(dep_id, app_id, user, status, environment):
    """Add a tier deployment for a given deployment ID"""

    app_dep = AppDeployments(dep_id, app_id, user, status, environment,
                             func.current_timestamp())

    # Commit to DB immediately
    Session.add(app_dep)
    Session.commit()

    return app_dep


def add_host_deployment(dep_id, host_id, user, status):
    """Add host deployment for a given host and deployment"""

    host_dep = HostDeployments(dep_id, host_id, user, status,
                               func.current_timestamp())

    # Commit to DB immediately
    Session.add(host_dep)
    Session.commit()

    return host_dep


def delete_host_deployment(hostname, project):
    """ """

    host_deps = (Session.query(HostDeployments)
                        .join(Hosts)
                        .join(Deployments)
                        .join(Packages)
                        .filter(Packages.pkg_name==project)
                        .filter(Hosts.hostname==hostname)
                        .all())

    # Allow this to silently do nothing if there are no matching rows
    for host_dep in host_deps:
        # Commit to DB immediately
        Session.delete(host_dep)
        Session.commit()


def delete_host_deployments(project, app_id, environment):
    """ """

    host_deps = (Session.query(HostDeployments)
                        .join(Hosts)
                        .join(Deployments)
                        .join(Packages)
                        .filter(Packages.pkg_name==project)
                        .filter(Hosts.app_id==app_id)
                        .filter(Hosts.environment==environment)
                        .all())

    for host_dep in host_deps:
        # Commit to DB immediately
        Session.delete(host_dep)
        Session.commit()


def find_all_app_deployments_by_apptype(project, apptype, environment):
    """Find all tier deployments for a given application type
       and specific environment
    """

    return (Session.query(AppDeployments)
                   .join(Deployments)
                   .join(Packages)
                   .join(AppDefinitions)
                   .filter(Packages.pkg_name==project)
                   .filter(AppDefinitions.app_type==apptype)
                   .filter(AppDeployments.environment==environment)
                   .all())


def find_app_deployment(pkg_id, app_ids, environment):
    """Find specific tier deployment(s) based on package ID and
       application ID(s)
    """

    subq = (Session.query(AppDeployments.app_id, AppDefinitions.app_type,
                          AppDeployments.id, Deployments.dep_type)
                   .join(Deployments)
                   .join(Packages)
                   .join(AppDefinitions)
                   .filter(Packages.id==pkg_id)
                   .filter(AppDeployments.app_id.in_(app_ids))
                   .filter(AppDeployments.environment==environment)
                   .order_by(AppDeployments.realized.desc())
                   .subquery(name='t_ordered'))

    return (Session.query(AppDeployments, AppDefinitions.app_type,
                          Deployments.dep_type, Packages)
                   .join(AppDefinitions)
                   .join(Deployments)
                   .join(Packages)
                   .join(subq, AppDeployments.id == subq.c.AppDeploymentID)
                   .group_by(subq.c.AppID)
                   .all())


def find_app_by_apptype(apptype):
    """Find a given application by app type"""

    try:
        return (Session.query(AppDefinitions)
                       .filter_by(app_type=apptype)
                       .one())
    except sqlalchemy.orm.exc.NoResultFound:
        raise DeployException('App type "%s" not found in the '
                              'app_definitions table' % apptype)


def find_app_by_depid(dep_id):
    """Find a given application and version by deployment ID"""

    try:
        return (Session.query(Packages)
                       .join(Deployments)
                       .filter(Deployments.id==dep_id)
                       .one())
    except sqlalchemy.orm.exc.NoResultFound:
        raise DeployException('No deployment with deploy ID "%s" found '
                              'in the deployments table' % dep_id)


def find_apptype_by_appid(app_id):
    """Find the app type for a given ID"""

    try:
        app_def = (Session.query(AppDefinitions)
                          .filter_by(id=app_id)
                          .one())
        return app_def.app_type
    except sqlalchemy.orm.exc.NoResultFound:
        raise DeployException('No app type with AppID "%s" was found '
                              'in the app_definitions table' % app_id)


def find_deployed_version(project, env, version=None, revision=None,
                          apptypes=None, apptier=False):
    """Find a given deployed version for a given project in a given
       environment for all related app types; search for full tier
       or host only deployment specifically
    """

    if apptier:
        subq = (Session.query(Packages.pkg_name,
                              Packages.version,
                              Packages.revision,
                              AppDefinitions.app_type,
                              AppDeployments.environment)
                       .join(Deployments)
                       .join(AppDeployments)
                       .join(AppDefinitions)
                       .filter(Packages.pkg_name==project)
                       .filter(AppDeployments.environment==env)
                       .filter(AppDeployments.status!='invalidated'))

        if apptypes is not None:
            subq = subq.filter(AppDefinitions.app_type.in_(apptypes))

        if version is not None:
            subq = subq.filter(Packages.version==version)

        if revision is not None:
            subq = subq.filter(Packages.revision==revision)

        subq = (subq.order_by(AppDeployments.realized.desc())
                    .subquery(name='t_ordered'))

        # The actual column name must be used in the subquery
        # usage below; DB itself should be corrected
        versions = (Session.query(subq.c.appType,
                                  subq.c.version,
                                  subq.c.revision)
                           .group_by(subq.c.appType, subq.c.environment)
                           .all())
    else:
        hostsq = (Session.query(Hosts.hostname, Hosts.app_id,
                                Packages.version, Packages.revision)
                         .join(AppDefinitions)
                         .join(HostDeployments)
                         .join(Deployments)
                         .join(Packages)
                         .filter(Packages.pkg_name==project)
                         .filter(Hosts.environment==env))

        if apptypes is not None:
            hostsq = hostsq.filter(AppDefinitions.app_type.in_(apptypes))

        versions = (hostsq.all())

    return versions


def find_deployment_by_id(dep_id):
    """Find deployment for a given ID"""

    try:
        return (Session.query(Deployments)
                       .filter_by(id=dep_id)
                       .one())
    except sqlalchemy.orm.exc.NoResultFound:
        raise DeployException('No deployment with deploy ID "%s" found '
                              'in the deployments table' % dep_id)


def find_deployment_by_pkgid(pkg_id):
    """Find deployment(s) for a given package ID"""

    return (Session.query(Deployments)
                   .filter_by(package_id=pkg_id)
                   .order_by(Deployments.declared.desc())
                   .all())


def find_host_by_hostname(hostname):
    """Find host for a given hostname"""

    try:
        return (Session.query(Hosts)
                       .filter_by(hostname=hostname)
                       .one())
    except sqlalchemy.orm.exc.NoResultFound:
        raise DeployException('No host with hostname "%s" found in '
                              'the hosts table' % hostname)


def find_host_deployment_by_depid(dep_id, dep_host):
    """Find host deployment (if exists) for a given deployment ID"""

    try:
        return (Session.query(HostDeployments)
                       .join(Hosts)
                       .filter(HostDeployments.deployment_id==dep_id)
                       .filter(Hosts.hostname==dep_host)
                       .one())
    except sqlalchemy.orm.exc.NoResultFound:
        # Currently this shouldn't be a fatal error
        return None


def find_host_deployments_by_pkgid(pkg_id, dep_hosts):
    """Find host deployments for a given package ID and a given
       set of hosts
    """

    return (Session.query(HostDeployments, Hosts.hostname, Hosts.app_id,
                          Deployments.dep_type)
                   .join(Hosts)
                   .join(Deployments)
                   .join(Packages)
                   .filter(Packages.id==pkg_id)
                   .filter(Hosts.hostname.in_(dep_hosts))
                   .all())


def find_host_deployments_by_project(project, dep_hosts):
    """Find host deployments for a given project and a given
       set of hosts
    """

    return (Session.query(HostDeployments, Hosts.hostname, Hosts.app_id,
                          Packages.version)
                   .join(Hosts)
                   .join(Deployments)
                   .join(Packages)
                   .filter(Packages.pkg_name==project)
                   .filter(Hosts.hostname.in_(dep_hosts))
                   .all())


def find_host_deployments_not_ok(pkg_id, app_id, environment):
    """Find host deployments that are not in 'ok' state for a given
       package ID, app ID and environment (may return none)
    """

    return (Session.query(HostDeployments, Hosts.hostname)
                   .join(Hosts)
                   .join(Deployments)
                   .filter(Deployments.package_id==pkg_id)
                   .filter(Hosts.app_id==app_id)
                   .filter(Hosts.environment==environment)
                   .filter(HostDeployments.status!='ok')
                   .all())


def find_hosts_for_app(app_id, environment):
    """Find the hosts for a given application and environment"""

    hosts = (Session.query(Hosts)
                    .join(AppDefinitions)
                    .filter(AppDefinitions.id==app_id)
                    .filter(Hosts.environment==environment)
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
                                  AppDefinitions.app_type.in_(apptypes)))
                          .all())

    return [ x[0] for x in rooms_query ]


def find_latest_deployed_version(project, env, apptypes=None, apptier=False):
    """Find the most recent deployed version for a given project
       in a given environment for all related app types; search
       for full tier or host only deployment specifically
    """

    return find_deployed_version(project, env, apptypes=apptypes,
                                 apptier=apptier)


def find_latest_validated_deployment(project, app_id, env):
    """Find the most recent deployment that was validated for a given
       project, application type and environment.
    """

    return (Session.query(AppDeployments, Packages.id)
                   .join(Deployments)
                   .join(Packages)
                   .filter(Packages.pkg_name==project)
                   .filter(AppDeployments.environment==env)
                   .filter(AppDeployments.status=='validated')
                   .order_by(AppDeployments.realized.desc())
                   .first())


def find_next_latest_validated_deployment(project, app_id, env):
    """Find the previously validated deployment (based on the current
       validated deployment) for a given project, application type
       and environment.
    """

    subq1 = (Session.query(Packages.pkg_name, Deployments.id)
                    .join(Deployments)
                    .join(AppDeployments)
                    .filter(Packages.pkg_name==project)
                    .filter(AppDeployments.app_id==app_id)
                    .filter(AppDeployments.environment==env)
                    .filter(AppDeployments.status=='validated')
                    .order_by(AppDeployments.realized.desc())
                    .subquery(name='t_ordered'))

    subq2 = (Session.query(subq1.c.DeploymentID)
                    .group_by(subq1.c.pkg_name)
                    .subquery(name='t_ordered2'))

    return (Session.query(AppDeployments, Packages.id)
                   .join(Deployments)
                   .join(Packages)
                   .filter(Packages.pkg_name==project)
                   .filter(AppDeployments.app_id==app_id)
                   .filter(AppDeployments.environment==env)
                   .filter(AppDeployments.status=='validated')
                   .filter(~Deployments.id.in_(subq2))
                   .order_by(AppDeployments.realized.desc())
                   .first())


def find_running_deployment(app_id, env, hosts=None):
    """Find a currently running tier or host deployment (or deployments)
       for a given application type and environment
    """

    tier = (Session.query(AppDeployments.user, AppDeployments.realized,
                          AppDeployments.environment, AppDefinitions.app_type)
                   .join(AppDefinitions)
                   .filter(AppDeployments.app_id==app_id)
                   .filter(AppDeployments.environment==env)
                   .filter(AppDeployments.status=='inprogress')
                   .order_by(AppDeployments.realized.desc())
                   .first())

    if tier:
        return ('tier', tier)

    host = (Session.query(HostDeployments.user, HostDeployments.realized,
                          Hosts.hostname, Hosts.environment)
                   .join(Hosts)
                   .filter(Hosts.environment==env)
                   .filter(Hosts.app_id==app_id)
                   .filter(HostDeployments.status=='inprogress')
                   .all())

    if host:
        return ('host', host)

    # Get here then nothing to return
    return None


def find_unvalidated_versions(time_delta, environment):
    """Find the latest deployments that are not validated in a given
       environment for a given amount of time
    """

    subq = (Session.query(Packages.pkg_name, Packages.version,
                          Packages.revision, AppDefinitions.app_type,
                          AppDeployments.environment, AppDeployments.realized,
                          AppDeployments.user, AppDeployments.status)
                   .join(Deployments)
                   .join(AppDeployments)
                   .join(AppDefinitions)
                   .filter(AppDeployments.status!='invalidated')
                   .filter(AppDeployments.environment==environment)
                   .order_by(AppDeployments.realized.desc())
                   .subquery(name='t_ordered'))

    return (Session.query(subq.c.pkg_name, subq.c.version, subq.c.revision,
                          subq.c.app_type, subq.c.environment,
                          subq.c.realized, subq.c.user, subq.c.status)
                   .group_by(subq.c.app_type, subq.c.environment,
                             subq.c.pkg_name)
                   .having(and_(subq.c.status.like('%complete'),
                                func.unix_timestamp(subq.c.realized) <
                                func.unix_timestamp(func.now()) - time_delta))
                   .all())


def list_app_deployment_info(project, env, app_type, version, revision):
    """Give all deployment information for a given project and version
       deployed to a given application tier and environment
    """

    return (Session.query(Deployments, AppDeployments, Packages)
                   .join(Packages)
                   .join(AppDeployments)
                   .join(AppDefinitions)
                   .filter(Packages.pkg_name==project)
                   .filter(Packages.version==version)
                   .filter(Packages.revision==revision)
                   .filter(AppDefinitions.app_type==app_type)
                   .filter(AppDeployments.environment==env)
                   .order_by(AppDeployments.realized.desc())
                   .first())


def list_host_deployment_info(project, env, version=None, revision=None,
                              apptypes=None):
    """Give all deployment information for a given project
       deployed to hosts for given (or all) application types
       and in given environment
    """

    dep_info = (Session.query(Deployments, HostDeployments, Hosts.hostname,
                              Packages)
                       .join(Packages)
                       .join(HostDeployments)
                       .join(Hosts)
                       .join(AppDefinitions))

    if version is not None:
        dep_info = dep_info.filter(Packages.version==version)

    if revision is not None:
        dep_info = dep_info.filter(Packages.revision==revision)

    if apptypes is not None:
        dep_info = dep_info.filter(AppDefinitions.app_type.in_(apptypes))

    return (dep_info.filter(Packages.pkg_name==project)
                    .filter(Hosts.environment==env)
                    .order_by(Hosts.hostname,
                              HostDeployments.realized.asc())
                    .all())
