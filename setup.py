"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

from codecs import open # to maintain consistent encoding. May or may not use. TODO: remove if unused
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'VERSION.txt'), encoding='utf-8') as f:
    version = f.read()

setup(name='street_names',
      version=version,
      description='Counts the Relative Prevalence of Street Names in the OpenMaps US Dataset',
      # The project's main homepage.
      url='https://www.github.com',
      author='Joshua Icuss',
      author_email='jicuss@gmail.com',
       # Choose your license
      license='',
      classifiers=[
        'Programming Language :: Python :: 2.7',
      ],
      packages=find_packages(exclude=['tests*','notes_do_not_include','logs','cache']),

      # Include non-python files found in each package in the install.
      include_package_data=True,

      package_data={
        # If any package contains *.json files, include them:
        '': ['*.json', '*.sql', ],
      },
      install_requires=['overpy','redis'],
      tests_require=['mock'],
      test_suite='tests',

      # List additional groups of dependencies here (e.g. development
      # dependencies). You can install these using the following syntax,
      # for example:
      # $ pip install -e .[dev,tests]
      extras_require={
        'dev': [
            'mock',
        ],
        'rel': [
            'mock',
            'wheel'
        ]
      },

      entry_points={
        'console_scripts': [
            'download_map_data=entry_points:downloadOpenMapData',
            'generate_faux_dataset=entry_points:generateFauxDatasetMain',
            'count_street_names=entry_points:countStreetNames',
        ],
      },

)