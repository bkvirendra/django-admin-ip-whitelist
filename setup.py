#!/usr/bin/env python

from setuptools import setup, find_packages

Version = '0.1.3'
setup(name='django-admin-ip-whitelist',
      version=Version,
      # install_requires='redis',
      description="Django middleware to allow access to /admin only for users, whose IPs are in the white list",
      long_description="django-admin-ip-whitelist is a django middleware app to allow access to /admin by IP addresses",
      author="dvska",
      url="http://github.com/dvska/django-admin-ip-whitelist",
      packages=find_packages(),
      license='Apache',
      platforms='Posix; MacOS X;',
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
     )
