import datetime

from .. import model as model


def seed():
    create_environments()
    # create_vlans()
    create_ganglia()
    create_applications()
    create_package_definitions()
    create_package_names()
    create_projects()
    create_project_packages()
    model.Session.commit()


def create_environments():
    for long in ('development', 'staging', 'production'):
        prefix = long[0]
        short = long[:4]
        domain = 'example-%s.org' % short

        model.Environment.update_or_create(dict(
            environment=long,
            env=short,
            domain=domain,
            prefix=prefix
        ))


def create_vlans():
    for env in model.Environment.all():
        model.Vlan.update_or_create(dict(
            name='%s-vlan' % env.env,
            description='for %s' % env.domain,
            environment=env,
        ))


def create_ganglia():
    model.Ganglia.update_or_create(dict(
        cluster_name='some-ganglia-thing'
    ))


def create_applications():
    prod = model.Environment.get_by(environment='production')
    dev = model.Environment.get_by(environment='development')
    stage = model.Environment.get_by(environment='staging')
    ganglia = model.Ganglia.first()
    for app_name in ('clamor', 'web', 'hubot'):
        model.Application.update_or_create(dict(
            app_type=app_name,
            host_base=app_name,
            puppet_class=app_name,
            ganglia_group_name='%s hosts' % app_name,
            description="%s application" % app_name,
            ganglia=ganglia,
            # production_vlan=prod.vlans[0],
            # development_vlan=dev.vlans[0],
            # staging_vlan=stage.vlans[0],
        ))


def create_package_definitions():
    for i in range(3):
        model.PackageDefinition.update_or_create(dict(
            deploy_type='some-deploy-type-%d' % i,
            validation_type='some-val-type-%d' % i,
            pkg_name='some-package-name-%d' % i,
            path='some-path-name-%d' % i,
            arch='x86_64',
            build_type='jenkins',
            build_host='ci.example.com',
            env_specific=False,
            created=datetime.datetime.now(),
        ))


def create_package_names():
    for pd in model.PackageDefinition.all():
        name = model.PackageName(name='name-for-%s' % pd.pkg_name)
        pd.package_names.append(name)


def create_projects():
    for name in ('clamor', 'web', 'hubot'):
        p = model.Project.update_or_create(dict(
            name='%s-project' % name
        ))


def create_project_packages():
    app_proj_pkgs = zip(
        model.Application.all(),
        model.Project.all(),
        model.PackageDefinition.all(),
    )

    for app, proj, pkg in app_proj_pkgs:
        x = model.ProjectPackage.update_or_create(dict(
            app_id=app.id,
            project_id=proj.id,
            pkg_def_id=pkg.id
        ), False)
