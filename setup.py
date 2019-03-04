from setuptools import setup
from autorm import version

version = '.'.join([str(x) for x in version])

setup(name='autorm',
      version=version,
      description="A minimal ORM",
      author="Sanket Sabnis",
      author_email="sanket@citizennet.com",
      url="http://github.com/citizennet/autorm",
      packages = ['autorm', 'autorm.db', 'autorm.tests'],
      package_data = {
        '': ['*.sql'],
    }
)
