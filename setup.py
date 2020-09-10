from time import time
from setuptools import setup
from setuptools import find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import call

long_description = open("README.md").read()
version = '1.0.%s' % int(time())


def install_spacy_model():
    "we need to download the spacy model and rebuild"
    call("python -m spacy download en_core_web_sm".split())
    call("python -m pip install -U spacy-lookups-data".split())


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        # post install of spacy model
        install_spacy_model()


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # post install of spacy model
        install_spacy_model()


setup(
    name='sitefab',
    version=version,
    description='State of the art static website generator for humans',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Elie Bursztein',
    author_email='code@elie.net',
    url='https://github.com/ebursztein/sitefab',
    license='Apache 2',
    entry_points={
        'console_scripts': ['sitefab=sitefab.cmdline.cmdline:main'],
    },
    cmdclass={
            'develop': PostDevelopCommand,
            'install': PostInstallCommand,
            },
    package_data={"": ["*.yaml"]},
    install_requires=[
            'Cython',
            'pyyaml',
            'jinja2',
            'tqdm',
            'termcolor',
            'yapsy',
            'gensim',
            'toposort',
            'Pygments',
            'pytz',
            'diskcache',
            'xxhash',
            'pillow',
            'perfcounters',
            'terminaltables',
            'textacy==0.10.1',
            'spacy==2.3.2',
            'mistune==0.8.4'],
    classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'Intended Audience :: Science/Research',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX :: Linux',
            'Topic :: Documentation',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Internet :: WWW/HTTP :: Site Management'],
    packages=find_packages())
