from setuptools import setup, find_packages
import os

version = '0.1'

test_requirements = ['mock', 'unittest2']
setup(name='collective.team',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Starzel.de',
      author_email='team@starzel.de',
      url='http://www.starzel.de',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'Products.CMFPlone',
        'plone.app.dexterity [grok]',
        'plone.app.referenceablebehavior',
        'plone.app.relationfield',
        'plone.namedfile [blobs]',
        'AccessControl',
        'Products.CMFCore',
        'Zope2',
        'plone.app.referenceablebehavior',
        'plone.behavior',
        'plone.directives.form',
        'plone.formwidget.autocomplete',
        'plone.principalsource',
        'rwproperty',
        'zope.interface',
        'zope.site',
        'z3c.autoinclude',
        ],
      extras_require = {
        'test': test_requirements},
      test_requires=test_requirements,
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
