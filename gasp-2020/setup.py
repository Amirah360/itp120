from setuptools import setup

setup(
    name='gasp',
    version='0.1.0',
    author= 'Gasp Development Team',
    author_email='',
    packages=['gasp'],
    url='https://gitlab.com/gasp-development-team/gasp-2020',
    license='gpl-3.0.md',
    description='A set of easy to use tools for creating games in Python 3',
    long_description=open('README.md').read(),
    install_requires=[
       "pygame >= 1.9.0",
   ],
)
