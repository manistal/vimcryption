from setuptools import setup

setup(
    # Packaging meta-data
    name='Vimcryption',
    version='0.1',
    description='Test package for VIMCryption VIM plugin.',
    author='Tom Manner, Miguel Nistal',
    author_email='tom.s.manner@gmail.com, nistam328@gmail.com',
    url='https://www.github.com/tsmanner/vimcryption',
    # Travis Unit-Test Installation
    install_requires=[
        'anybadge==0.1.0.dev2',
        'codecov',
        'coverage>=4.5',
        'coverage-badge',
        'nose2',
        'nose2[coverage_plugin]>=0.6.5',
        'numpy',
        'pylint',
    ],
    packages=[
        'encryptionengine',
    ],
)
