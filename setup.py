import codecs
from setuptools import setup, find_packages

entry_points = {
    'console_scripts': [
    ],
}

TESTS_REQUIRE = [
    'nti.testing',
    'zope.testrunner',
]


def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()


setup(
    name='nti.messaging',
    version=_read('version.txt').strip(),
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="NTI Messaging",
    long_description=(_read('README.rst') + '\n\n' + _read('CHANGES.rst')),
    license='Apache',
    keywords='Messaging',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    zip_safe=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    namespace_packages=['nti'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'setuptools',
        'six',
        'nti.base',
        'nti.containers',
        'nti.coremetadata',
        'nti.dublincore',
        'nti.externalization',
        'nti.mimetype',
        'nti.namedfile',
        'nti.property',
        'nti.schema',
        'nti.threadable',
        'nti.zope_catalog',
        'ZODB',
        'zope.annotation',
        'zope.cachedescriptors',
        'zope.component',
        'zope.container',
        'zope.intid',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.location',
        'zope.schema',
        'zope.security',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
    },
    entry_points=entry_points,
    test_suite="nti.messaging.tests",
)
