from setuptools import setup

# Let's add this later
# long_description = open('README.txt').read()

# Get version of project
execfile('tagopsdb/version.py')

setup_args = dict(
    name = 'tagopsdb',
    version = __version__,
    description = 'Python library to interface with TagOps database',
    # long_description = long_description,
    author = 'Kenneth Lareau',
    author_email = 'klareau@tagged.com',
    license = 'MIT',
    packages = ['tagopsdb', 'tagopsdb.database', 'tagopsdb.deploy'],
    scripts = [],
)

if __name__ == '__main__':
    setup(**setup_args)
