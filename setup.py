from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in szamlazz_agent_connector/__init__.py
from szamlazz_agent_connector import __version__ as version

setup(
	name='szamlazz_agent_connector',
	version=version,
	description='App for connecting to szamlazz.hu.',
	author='coding.pensav.hu',
	author_email='coding@pensav.hu',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
