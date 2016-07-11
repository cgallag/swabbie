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
    version='0.1.4',
    packages=find_packages(),
    description='Helps manage your docker environment',
    url='https://github.com/cgallag/swabbie',
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        swabbie=swabbie.run:cli
    ''',
    author='Caroline Gallagher',
    author_email='caroline@rokoid.com',
    keywords=['docker', 'clean', 'nuke', 'dangling images'],
    long_description=read("README.rst"),
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ]
)