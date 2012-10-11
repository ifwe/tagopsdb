import sqlalchemy.orm.exc

from tagopsdb.database.meta import Session
from tagopsdb.database.model import AppDefinitions, AppPackages, \
                                    PackageLocations
from tagopsdb.exceptions import RepoException


def add_app_location(project_type, pkg_type, pkg_name, app_name, path,
                     build_host, environment):
    """Add the location of a given application"""

    # Ensure the environment parameter is boolean
    if environment:
        environment = True
    else:
        environment = False

    app = PackageLocations(project_type, pkg_type, pkg_name, app_name, path,
                           build_host, environment)
    Session.add(app)
    Session.flush()   # Needed to get pkgLocationID generated

    return app.pkgLocationID


def add_app_packages_mapping(pkg_location_id, app_types):
    """Add the mappings of the app types for each package"""

    for app_type in app_types:
        try:
            app_def = (Session.query(AppDefinitions)
                              .filter_by(appType=app_type)
                              .one())
        except sqlalchemy.orm.exc.NoResultFound:
            raise RepoException('App type "%s" is not found in the '
                                'AppDefinitions table' % app_type)

        app_pkg = AppPackages(pkg_location_id, app_def.AppID)
        Session.add(app_pkg)


def delete_app_location(app_name):
    """Delete the location of a given application"""

    try:
        app = list_app_location(app_name)
    except sqlalchemy.orm.exc.NoResultFound:
        raise RepoException('No application "%s" to remove from '
                            'PackageLocations table' % app_name)

    Session.delete(app)


def find_app_packages_mapping(app_name):
    """Find all app types related to a given package"""

    app_defs = (Session.query(AppDefinitions)
                       .join(AppPackages)
                       .join(PackageLocations)
                       .filter(PackageLocations.app_name==app_name)
                       .all())

    if not app_defs:
        raise RepoException('No entries found for project "%s" in '
                            'in AppPackages table' % app_name)

    return app_defs


def list_app_location(app_name):
    """ """

    return (Session.query(PackageLocations)
                   .filter_by(app_name=app_name)
                   .one())


def list_all_app_locations():
    """ """

    return (Session.query(PackageLocations)
                   .order_by(PackageLocations.app_name)
                   .all())
