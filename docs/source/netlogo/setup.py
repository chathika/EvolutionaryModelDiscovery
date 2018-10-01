"""Implementation of a Pygments Lexer for the NetLogo."""

from setuptools import setup

__author__ = 'Jan C. Thiele'

setup(
    name='NetLogo Pygments Lexer',
    version='0.1.2',
    #description=__doc__,
    description="NetLogo syntax colorer using Pygments",
    author=__author__,
    author_email='jthiele@gwdg.de',
    url='http://',
    license='GPL',
    packages=['netlogo'],
    #install_requires=[
    #    'Pygments >= 1.2',
    #],
    include_package_data=True,
    zip_safe=True,
    entry_points='''
    [pygments.lexers]
    NetLogo = netlogo:NetLogoLexer
    [pygments.styles]
    NetLogo = netlogo:NetLogoStyle
    '''
)
