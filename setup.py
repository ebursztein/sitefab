from time import time
from setuptools import setup
from setuptools import find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import call

long_description = open("README.md").read()
version = '1.2.%s' % int(time())


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
    setup_requires=["Cython"],
    install_requires=[
            'blis==0.7.9',
            'cachetools==5.3.0',
            'certifi==2022.12.7',
            'charset-normalizer==3.1.0',
            'click==8.1.3',
            'catalogue==2.0.8',
            'confection==0.0.4',
            'cymem==2.0.7',
            'cytoolz==0.12.1',
            'diskcache==5.4.0',
            'gensim==4.3.1',
            'idna==3.4',
            'jellyfish==0.9.0',
            'Jinja2==3.1.2',
            'joblib==1.2.0',
            'langcodes==3.3.0',
            'MarkupSafe==2.1.2',
            'mistune==2.0.5',
            'murmurhash==1.0.9',
            'networkx==3.0',
            'numpy==1.24.2',
            'packaging==23.0',
            'pathy==0.10.1',
            'perfcounters==2.1.0',
            'Pillow==9.4.0',
            'preshed==3.0.8',
            'pydantic==1.10.7',
            'Pygments==2.14.0',
            'pyphen==0.14.0',
            'pytz==2022.7.1',
            'PyYAML==6.0',
            'requests==2.28.2',
            'scikit-learn==1.2.2',
            'scipy==1.10.1',
            'smart-open==6.3.0',
            'spacy==3.5.1',
            'spacy-legacy==3.0.12',
            'spacy-loggers==1.0.4',
            'spacy-lookups-data==1.0.3',
            'srsly==2.4.6',
            'tabulate==0.9.0',
            'termcolor==2.2.0',
            'terminaltables==3.1.10',
            'textacy==0.12.0',
            'thinc==8.1.9',
            'threadpoolctl==3.1.0',
            'toolz==0.12.0',
            'toposort==1.10',
            'tqdm==4.65.0',
            'typer==0.7.0',
            'typing_extensions==4.5.0',
            'urllib3==1.26.15',
            'wasabi==1.1.1',
            'xxhash==3.2.0',
            'Yapsy==1.12.2',
            ],
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
