import time
import tagopsdb


def discover_models():
    classes = []

    for clsname in vars(tagopsdb).keys():
        cls = getattr(tagopsdb, clsname)
        if not isinstance(cls, type):
            continue
        if not issubclass(cls, tagopsdb.Base) or cls is tagopsdb.Base:
            continue

        classes.append(cls)

    classes.sort(key=lambda x: x.__name__)
    return classes


def test_model_and_direct_relationships(cls):
    obj = cls.first()
    if obj is None:
        raise Exception('got None for %r', cls.__name__)

    print cls.__name__ + ':', obj

    for rel in obj.mapper.relationships:
        val = getattr(obj, rel.key, None)
        try:
            val = iter(val).next()
        except TypeError:
            pass
        except StopIteration:
            print Exception(
                'collection was empty! %s.%s',
                cls.__name__,
                rel.key
            )

        if val is None:
            print Exception('got None for %r on %r', rel.key, obj)

        print '\t'+rel.key+':', val


def write_schema():
    import sqlalchemy
    import elixir

    engine = None
    f = None

    with open('schema.mysql.txt', 'w') as f:
        def executor(s, p=';'):
            compiled = s.compile(dialect=engine.dialect)
            f.write(unicode(compiled).encode('utf8') + p)

        engine = sqlalchemy.create_engine(
            'mysql+oursql://',
            strategy='mock',
            executor=executor
        )
        elixir.metadata.bind = engine
        elixir.setup_all()
        elixir.create_all()


def create_environments():
    for long in ('development', 'staging', 'production'):
        prefix = long[0]
        short = long[:4]
        domain = 'example-%s.org' % short

        tagopsdb.Environment.update_or_create(dict(
            environment=long,
            env=short,
            domain=domain,
            prefix=prefix
        ))


def create_vlans():
    for env in tagopsdb.Environment.all():
        tagopsdb.Vlan.update_or_create(dict(
            name='%s-vlan' % env.env,
            description='for %s' % env.domain,
            environment=env,
        ))


def create_ganglia():
    tagopsdb.Ganglia.update_or_create(dict(
        cluster_name='some-ganglia-thing'
    ))


def create_applications():
    prod = tagopsdb.Environment.get_by(environment='production')
    dev = tagopsdb.Environment.get_by(environment='development')
    stage = tagopsdb.Environment.get_by(environment='staging')
    ganglia = tagopsdb.Ganglia.first()
    for app_name in ('clamor', 'web', 'hubot'):
        tagopsdb.Application.update_or_create(dict(
            name=app_name,
            host_base=app_name,
            puppet_class=app_name,
            ganglia_group_name='%s hosts' % app_name,
            description="%s application" % app_name,
            ganglia=ganglia,
            production_vlan=prod.vlans[0],
            development_vlan=dev.vlans[0],
            staging_vlan=stage.vlans[0],
        ))


def test():
    proj = tagopsdb.Project(name='abuse-finder-project')
    pkg_def = tagopsdb.PackageDefinition(
        deploy_type='rpm',
        validation_type='matching',
        name='abuse-finder-name',
        path='abuse-finder-path',
        arch='noarch',
        build_type='jenkins',
        build_host='javabuild',
        env_specific=0,
    )
    name = tagopsdb.PackageName(
        name='abuse-finder-package-name',
        package_definition=pkg_def
    )

    loc = tagopsdb.PackageLocation(
        name=pkg_def.name,
        path=pkg_def.path,
        arch=pkg_def.arch,
        pkg_type=pkg_def.build_type,
        build_host=pkg_def.build_host,
        environment=pkg_def.env_specific,
        app_name='abuse-finder-app',
        project_type='application',
    )

    proj.package_definitions.append(pkg_def)
    proj.apps.append(tagopsdb.Application.first())
    elixir.session.commit()


if __name__ == '__main__':
    try:
        tagopsdb.init(
            url=dict(
                username='tds',
                password='bleepbloop',
                host='localhost',
                database='tds_%s' % int(time.time()),
            ),
            pool_recycle=3600,
            create=True,
        )

        import elixir
        # elixir.metadata.bind.echo = True

        create_environments()
        create_vlans()
        create_ganglia()
        create_applications()
        test()
        # import code
        # code.interact(local=locals())
    finally:
        elixir.metadata.bind.echo = False
        tagopsdb.destroy()
