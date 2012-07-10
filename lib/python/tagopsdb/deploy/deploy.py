import sqlalchemy.orm.exc

from sqlalchemy.sql.expression import func

from tagopsdb.database.meta import Session
from tagopsdb.database.model import AppDefinitions, Deployments, Packages
from tagopsdb.exceptions import DeployException, NotImplementedException


def find_deployment(pkg_id, app_id, declaration, environment):
    """Find a specific deployment (keyed on declaration)"""

    try:
        (Session.query(Deployments)
                .filter_by(PackageID=pkg_id)
                .filter_by(AppID=app_id)
                .filter_by(declaration=declaration)
                .filter_by(environment=environment)
                .one())
    except sqlalchemy.orm.exc.NoResultFound:
        return False
    else:
        return True


def get_deployment_by_id(dep_id):
    """Get deployment information based on given ID"""

    try:
        return (Session.query(Deployments)
                       .filter_by(DeploymentID=dep_id)
                       .one())
    except sqlalchemy.orm.exc.NoResultFound:
        raise DeployException('No deployment with deploy ID "%s" exists '
                              'in the database' % dep_id)


def invalidate_deployment(deployment, declarer):
    """ """

    if find_deployment(deployment.PackageID, deployment.AppID, 'invalidate',
                       deployment.environment):
        raise DeployException('Given deployment already invalidated '
                              'in database')

    dep = Deployments(declarer = declarer,
                      declared = func.current_timestamp(),
                      PackageID = deployment.PackageID,
                      AppID = deployment.AppID,
                      declaration = 'invalidate',
                      environment = deployment.environment)
    Session.add(dep)


def list_deployment_info(project, version, revision=None):
    """ """

    return (Session.query(Deployments, Packages, AppDefinitions.appType)
                   .join(Packages)
                   .join(AppDefinitions)
                   .filter(Packages.pkg_name==project)
                   .filter(Packages.version==version)
                   .order_by(AppDefinitions.appType,
                             Deployments.declared.desc())
                   .all())


def validate_deployment(deployment, declarer):
    """ """

    if find_deployment(deployment.PackageID, deployment.AppID, 'validate',
                       deployment.environment):
        raise DeployException('Given deployment already validated '
                              'in database')

    dep = Deployments(declarer = declarer,
                      declared = func.current_timestamp(),
                      PackageID = deployment.PackageID,
                      AppID = deployment.AppID,
                      declaration = 'validate',
                      environment = deployment.environment)
    Session.add(dep)
