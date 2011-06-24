from setuptools import setup
import os
data_files = []

for dirpath, dirnames, filenames in os.walk('social'):
  for i, dirname in enumerate(dirnames):
    if dirname.startswith('.'): del dirnames[i]
  if not '__init__.py' in filenames and filenames:
    data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

print data_files

files = []

#print files
try:
    from setuptools import setup, find_packages, Command
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages, Command

from setuptools import findall
files = findall()

import os
for f in files:
  if '.svn' in os.path.split(f):
    print 'bad!', f
  else: f
files = []

install_requires = []

try:
    __import__('uuid')
except ImportError:
    install_requires.append('uuid')

#files=["progressable/*"]

packages = find_packages(exclude=('example', 'example.*'))

setup(
        name="django-hyves",
        version="0.2.1",
        description="Port of the hyves PHP library genus to python + basic django implementation",
        author="Jacco Flenter @ Secret Code Machine",
        author_email="jacco(_AT_)secretcodemachine.com",
        packages = packages,
        data_files = data_files,
        include_package_data=True,
        long_description = """
        A port of the php library genus for the (dutch) social network site Hyves 

        It consists of 3 parts:
        * genus, genus.oauth (namespace) the port of the library
        * social, a basic django implementation including some decorators who 
        are the projects equivolent of login_required
        * example, a small django project using this.

        See the example project for all dependencies
        """,
        license="BSD",
        keywords="Hyves, python, django, oauth, genus, social network",
        url='https://github.com/flenter/django-hyves/',
        classifiers = [
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: BSD License",
        ],
    )

