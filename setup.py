import codecs
import os

from setuptools import setup, find_packages


HERE = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()

setup(
    name='swabbie',
    version='0.1',
    packages=find_packages(),
    description='Helps manage your docker environment',
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        swabbie=swabbie.run:cli
    ''',
    author='Caroline Gallagher',
    keywords=['docker', 'clean', 'nuke', 'dangling images'],
    long_description=read("README.rst"),
    license='MIT',
)