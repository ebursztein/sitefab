from setuptools import setup
from setuptools import find_packages

long_description = open("README.md").read()
version = '2.0.0'
setup(name='sitefab',
      version=version,
      description='A flexible yet simple website static generator for humans',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Elie Bursztein',
      author_email='code@elie.net',
      url='https://github.com/ebursztein/sitefab',
      license='Apache 2',
      install_requires=['pyyaml',
                        'jinja2',
                        'tqdm',
                        'termcolor',
                        'yapsy',
                        'gensim',
                        '3to2',
                        'toposort',
                        'Pygments',
                        'pytz',
                        'diskcache',
                        'stop-words',
                        'xxhash',
                        'pillow',
                        'perfcounters',
                        'terminaltables'
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
          'Topic :: Internet :: WWW/HTTP :: Site Management'
      ],
      packages=find_packages())
