import sys
from setuptools import setup
from setuptools import find_packages

version = '1.0'

install_requires = [
    'setuptools',
    'venusian',
    ]

if sys.version_info < (2, 7):
    install_requires.append('argparse')

setup(name='s4u.upgrade',
      version=version,
      description='2Style4You upgrade framework',
      long_description=open('README.rst'),
      author='Simplon B.V. - Wichert Akkerman',
      author_email='wichert@wiggy.net',
      url='http://www.2style4you.com/',
      license='BSD',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      namespace_packages=['s4u'],
      zip_safe=False,
      install_requires=install_requires,
      test_suite='s4u.upgrade',
      entry_points='''
      [console_scripts]
      upgrade = s4u.bfgtools.upgrade:upgrade
      ''')
