import sqlalchemy.orm.exc

from sqlalchemy.sql.expression import func

from tagopsdb.database.meta import Session
from tagopsdb.database.model import AppDefinitions, AppDeployments, \
                                    Deployments, HostDeployments, Hosts, \
                                    Packages
from tagopsdb.exceptions import DeployException, NotImplementedException


def add_deployment(pkg_id, user, dep_type):
    """Add deployment for a given package ID"""

    dep = Deployments(pkg_id, user, dep_type, func.current_timestamp())

    # Commit to DB immediately
    Session.begin_nested()
    Session.add(dep)
    Session.commit()

    # Following line may not longer be needed?
    Session.flush()   # Needed to get DeploymentID generated

    return dep


def add_app_deployment(dep_id, app_id, user, status, environment):
    """Add a tier deployment for a given deployment ID"""

    app_dep = AppDeployments(dep_id, app_id, user, status, environment,
                             func.current_timestamp())

    # Commit to DB immediately
    Session.begin_nested()
    Session.add(app_dep)
    Session.commit()

    return app_dep


def add_host_deployment(dep_id, host_id, user, status):
    """Add host deployment for a given host and deployment"""

    host_dep = HostDeployments(dep_id, host_id, user, status,
                               func.current_timestamp())

    # Commit to DB immediately
    Session.begin_nested()
    Session.add(host_dep)
    Session.commit()

    return host_dep


def delete_host_deployment(hostname):
    """ """

    host_deps = (Session.query(HostDeployments)
                        .join(Hosts)
                        .filter(Hosts.hostname==hostname)
                        .all())

    # Allow this to silently do nothing if there are no matching rows
    for host_dep in host_deps:
        # Commit to DB immediately
        Session.begin_nested()
        Session.delete(host_dep)
        Session.commit()


def delete_host_deployments(app_id, environment):
    """ """

    host_deps = (Session.query(HostDeployments)
                        .join(Hosts)
                        .filter(Hosts.AppID==app_id)
                        .filter(Hosts.environment==environment)
                        .all())

    for host_dep in host_deps:
        # Commit to DB immediately
        Session.begin_nested()
        Session.delete(host_dep)
        Session.commit()


def find_app_deployment(pkg_id, app_ids, environment):
    """Find specific tier deployment(s) based on package ID and
       application ID(s)
    """

    subq = (Session.query(AppDeployments.AppID, AppDefinitions.appType,
                          AppDeployments.AppDeploymentID,
                          Deployments.dep_type)
                   .join(Deployments)
                   .join(Packages)
                   .join(AppDefinitions)
                   .filter(Packages.PackageID==pkg_id)
                   .filter(AppDeployments.AppID.in_(app_ids))
                   .filter(AppDeployments.environment==environment)
                   .order_by(AppDeployments.realized.desc())
                   .subquery(name='t_ordered'))

    return (Session.query(AppDeployments, AppDefinitions.appType,
                          Deployments.dep_type, Packages)
                   .join(AppDefinitions)
                   .join(Deployments)
                   .join(Packages)
                   .join(subq, AppDeployments.AppDeploymentID ==
                               subq.c.AppDeploymentID)
                   .group_by(subq.c.AppID)
                   .all())


def find_app_by_apptype(apptype):
    """Find a given application by app type"""

    try:
        return (Session.query(AppDefinitions)
                       .filter_by(appType=apptype)
                       .one())
    except sqlalchemy.orm.exc.NoResultFound:
        raise DeployException('App type "%s" not found in the '
                              'app_definitions table' % apptype)


def find_app_by_depid(dep_id):
    """Find a given application and version by deployment ID"""

    try:
        return (Session.query(Packages)
                       .join(Deployments)
                       .filter(Deployments.DeploymentID==dep_id)
                       .one())
    except sqlalchemy.orm.exc.NoResultFound:
        raise DeployException('No deployment with deploy ID "%s" found '
                              'in the deployments table' % dep_id)


def find_deployment_by_id(dep_id):
    """Find deployment for a given ID"""

    try:
        return (Session.query(Deployments)
                       .filter_by(DeploymentID=dep_id)
                       .one())
    except sqlalchemy.orm.exc.NoResultFound:
        raise DeployException('No deployment with deploy ID "%s" found '
                              'in the deployments table' % dep_id)


def find_deployment_by_pkgid(pkg_id):
    """Find deployment(s) for a given package ID"""

    return (Session.query(Deployments)
                   .filter_by(PackageID=pkg_id)
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
                       .filter(HostDeployments.DeploymentID==dep_id)
                       .filter(Hosts.hostname==dep_host)
                       .one())
    except sqlalchemy.orm.exc.NoResultFound:
        # Currently this shouldn't be a fatal error
        return None


def find_host_deployments_by_pkgid(pkg_id, dep_hosts):
    """Find host deployments for a given package ID and a given
       set of hosts
    """

    return (Session.query(HostDeployments, Hosts.hostname, Hosts.AppID,
                          Deployments.dep_type)
                   .join(Hosts)
                   .join(Deployments)
                   .join(Packages)
                   .filter(Packages.PackageID==pkg_id)
                   .filter(Hosts.hostname.in_(dep_hosts))
                   .all())


def find_host_deployments_by_project(project, dep_hosts):
    """Find host deployments for a given project and a given
       set of hosts
    """

    return (Session.query(HostDeployments, Hosts.hostname, Hosts.AppID,
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
                   .join(Deployments)
                   .filter(Deployments.PackageID==pkg_id)
                   .filter(Hosts.AppID==app_id)
                   .filter(Hosts.environment==environment)
                   .filter(HostDeployments.status!='ok')
                   .all())


def find_hosts_for_app(app_id, environment):
    """Find the hosts for a given application and environment"""

    hosts = (Session.query(Hosts)
                    .join(AppDefinitions)
                    .filter(AppDefinitions.AppID==app_id)
                    .filter(Hosts.environment==environment)
                    .all())

    if not hosts:
        raise DeployException('No hosts found for AppID "%s" in '
                              'environment "%s" in the database'
                              % (app_id, environment))

    return hosts


def find_deployed_version(project, env, version=None, revision=None,
                          apptier=False):
    """Find a given deployed version for a given project in a given
       environment for all related app types; search for full tier
       or host only deployment specifically
    """

    if apptier:
        subq = (Session.query(Packages.pkg_name,
                              Packages.version,
                              Packages.revision,
                              AppDefinitions.appType,
                              AppDeployments.environment)
                       .join(Deployments)
                       .join(AppDeployments)
                       .join(AppDefinitions)
                       .filter(Packages.pkg_name==project)
                       .filter(AppDeployments.environment==env)
                       .filter(AppDeployments.status!='invalidated'))

        if version is not None:
            subq = subq.filter(Packages.version==version)

        if revision is not None:
            subq = subq.filter(Packages.revision==revision)

        subq = (subq.order_by(AppDeployments.realized.desc())
                    .subquery(name='t_ordered'))

        versions = (Session.query(subq.c.appType,
                                  subq.c.version,
                                  subq.c.revision)
                           .group_by(subq.c.appType, subq.c.environment)
                           .all())
    else:
        versions = (Session.query(Hosts.hostname, Packages.version,
                                  Packages.revision)
                           .join(HostDeployments)
                           .join(Deployments)
                           .join(Packages)
                           .filter(Packages.pkg_name==project)
                           .filter(Hosts.environment==env)
                           .all())

    return versions


def find_latest_deployed_version(project, env, apptier=False):
    """Find the most recent deployed version for a given project
       in a given environment for all related app types; search
       for full tier or host only deployment specifically
    """

    if apptier:
        subq = (Session.query(Packages.pkg_name,
                              Packages.version,
                              Packages.revision,
                              AppDefinitions.appType,
                              AppDeployments.environment)
                       .join(Deployments)
                       .join(AppDeployments)
                       .join(AppDefinitions)
                       .filter(Packages.pkg_name==project)
                       .filter(AppDeployments.environment==env)
                       .filter(AppDeployments.status!='invalidated')
                       .order_by(AppDeployments.realized.desc())
                       .subquery(name='t_ordered'))

        versions = (Session.query(subq.c.appType,
                                  subq.c.version,
                                  subq.c.revision)
                           .group_by(subq.c.appType, subq.c.environment)
                           .all())
    else:
        versions = (Session.query(Hosts.hostname, Packages.version,
                                  Packages.revision)
                           .join(HostDeployments)
                           .join(Deployments)
                           .join(Packages)
                           .filter(Packages.pkg_name==project)
                           .filter(Hosts.environment==env)
                           .all())

    return versions


def find_latest_validated_deployment(project, app_id, env):
    """Find the most recent deployment that was validated for a given
       project, application type and environment.
    """

    return (Session.query(AppDeployments, Packages.PackageID)
                   .join(Deployments)
                   .join(Packages)
                   .filter(Packages.pkg_name==project)
                   .filter(AppDeployments.AppID==app_id)
                   .filter(AppDeployments.environment==env)
                   .filter(AppDeployments.status=='validated')
                   .order_by(AppDeployments.realized.desc())
                   .first())


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
                   .filter(AppDefinitions.appType==app_type)
                   .filter(AppDeployments.environment==env)
                   .order_by(AppDeployments.realized.desc())
                   .first())


def list_host_deployment_info(project, env, version=None, revision=None):
    """Give all deployment information for a given project
       deployed to hosts in given environment
    """

    dep_info = (Session.query(Deployments, HostDeployments, Hosts.hostname,
                              Packages)
                       .join(Packages)
                       .join(HostDeployments)
                       .join(Hosts))

    if version is not None:
        dep_info = dep_info.filter(Packages.version==version)

    if revision is not None:
        dep_info = dep_info.filter(Packages.revision==revision)

    return (dep_info.filter(Packages.pkg_name==project)
                    .filter(Hosts.environment==env)
                    .order_by(Hosts.hostname,
                              HostDeployments.realized.asc())
                    .all())
