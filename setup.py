#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# ugly pytest class definition...
try:
    from setuptools import setup
    from setuptools.command.test import test as TestCommand

    class PyTest(TestCommand):
        def finalize_options(self):
            TestCommand.finalize_options(self)
            self.test_args = []
            self.test_suite = True

        def run_tests(self):
            #import here, cause outside the eggs aren't loaded
            import pytest
            errno = pytest.main(self.test_args)
            sys.exit(errno)

except ImportError:
    from distutils.core import setup, Command

    class PyTest(Command):
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            import sys
            import subprocess
            errno = subprocess.call([sys.executable, 'runtests.py'])
            raise SystemExit(errno)

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')
with open('requirements.txt') as f:
    reqs = f.read().splitlines()

#install_reqs = parse_requirements("requirements.txt")
#reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='track_a_parcel',
    version='0.1.0',
    description='Application to track parcels using the CLI',
    long_description=readme + '\n\n' + history,
    author='Matthieu Falce',
    author_email='falce.matthieu@gmail.com',
    url='https://github.com/ice3/track_a_parcel',
    packages=[
        'track_a_parcel',
    ],
    package_dir={'track_a_parcel': 'track_a_parcel'},
    include_package_data=True,
    install_requires=reqs,
    license="BSD",
    zip_safe=False,
    keywords='track_a_parcel',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    #test_suite='tests',
    tests_require=['pytest'],
    cmdclass={'test': PyTest}
)
