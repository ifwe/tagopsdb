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

if __name__ == '__main__':
    tagopsdb.init(
        url=dict(
            username='tagopsdb_reader',
            password='kitties',
            host='opsdb.tagged.com',
        ),
        pool_recycle=3600
    )

    classes = discover_models()
    print '%d classes discovered' % len(classes)
    for cls in classes:
        test_model_and_direct_relationships(cls)
        print '-' * 80
