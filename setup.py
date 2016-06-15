from setuptools import setup

setup(
    name='swabbie',
    version='0.1',
    py_modules=['swabbie'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        swabbie=swabbie:cli
    ''',
)