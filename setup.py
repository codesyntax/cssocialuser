from setuptools import setup, find_packages
import sys, os

version = '0.33'

setup(name='cssocialuser',
      version=version,
      description="CsSocialUser",
      long_description="""\
Social users compatible with Django>=1.5""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Jatsu Argarate',
      author_email='jargarate@codesyntax.com',
      url='https://github.com/codesyntax/cssocialuser',
      license='New BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      requires=['django(>=1.5)'],
      install_requires=[
          # -*- Extra requirements: -*-
          'django-social-auth',
          'django-registration-redux',
          'tweepy',
          'facebook-sdk',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
