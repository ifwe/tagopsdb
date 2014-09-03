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
        environment=False,
        app_name='abuse-finder-app',
        project_type='application',
    )

    proj.package_definitions.append(pkg_def)
    proj.apps.append(tagopsdb.Application.first())
    tagopsdb.Session.commit()


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

        create_environments()
        create_vlans()
        create_ganglia()
        create_applications()
        test()
        # import code
        # code.interact(local=locals())
    finally:
        tagopsdb.destroy()
