from setuptools import setup

setup(
  name='jizera',
  version='211208',
  packages=['jizera'],
  package_data={
    'jizera': ['static/*', 'templates/*']
  },
  install_requires=[
    'flask==2.0.2',
  ],
  zip_safe=False,
)

