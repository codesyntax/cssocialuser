from setuptools import setup, find_packages
import sys, os

version = '0.31'

setup(name='cssocialuser',
      version=version,
      description="CsSocialUser",
      long_description="""\
Django 1.5ak earri dituen aldaketak inplementatzeko""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Jatsu Argarate',
      author_email='jargarate@codesyntax.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'django-social-auth',
          'django_registration_redux',
          'tweepy',
          'facebook-sdk',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
