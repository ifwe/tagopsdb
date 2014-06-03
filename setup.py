from setuptools import setup
from setuptools.command.test import test as TestCommand

import sys

# Let's add this later
# long_description = open('README.txt').read()

# Get version of project
import version


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [self.test_suite]

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        if errno != 0:
            raise SystemExit("Test failures (errno=%d)", errno)


PYTHON27_REQ_BLACKLIST = ['argparse', 'ordereddict']


def reqfile_read(fname):
    with open(fname, 'r') as reqfile:
        reqs = reqfile.read()

    return filter(None, reqs.strip().splitlines())


def load_requirements(fname):
    requirements = []

    for req in reqfile_read(fname):
        if 'git+' in req:
            req = '=='.join(req.rsplit('=')[-1].rsplit('-', 1))
        if sys.version_info > (2, 7) or sys.version_info > (3, 2):
            if any(req.startswith(bl) for bl in PYTHON27_REQ_BLACKLIST):
                continue
        requirements.append(req)

    return requirements


def load_github_dependency_links(fname):
    dep_links = []
    for req in reqfile_read(fname):
        if 'git+' in req and 'github' in req:  # not exactly precise...
            url, ref_egg = req.split('git+', 1)[-1].rsplit('@', 1)
            dep_links.append(url + '/tarball/' + ref_egg)

    return dep_links

REQUIREMENTS = {}
REQUIREMENTS['install'] = load_requirements('requirements.txt')
REQUIREMENTS['tests'] = load_requirements('requirements-dev.txt')

DEPENDENCY_LINKS = load_github_dependency_links('requirements.txt')
DEPENDENCY_LINKS.extend(load_github_dependency_links('requirements-dev.txt'))

setup_args = dict(
    name='tagopsdb',
    version=version.__version__,
    description='Python library to interface with TagOps database',
    # long_description = long_description,
    author='Kenneth Lareau',
    author_email='klareau@tagged.com',
    license='MIT',
    packages=[
        'tagopsdb',
        'tagopsdb.database',
        'tagopsdb.deploy',
        'tagopsdb.model',
        'tagopsdb.model.meta',
    ],
    entry_points={},
    install_requires=REQUIREMENTS['install'],
    test_suite='tests',
    tests_require=REQUIREMENTS['tests'] + REQUIREMENTS['install'],
    cmdclass=dict(test=PyTest),
    dependency_links=DEPENDENCY_LINKS,
)

if __name__ == '__main__':
    setup(**setup_args)
