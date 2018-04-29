from setuptools import setup

setup(
    # Packaging meta-data
    name='Vimcryption',
    version='0.1',
    description='Python library with encryption engines used by vimcryption.',
    author='Tom Manner, Miguel Nistal',
    author_email='tom.s.manner@gmail.com, nistam328@gmail.com',
    url='https://www.github.com/tsmanner/vimcryption',
    # Installation
    install_requires=[
        'numpy',
    ],
    packages=[
        'encryptionengine',
    ],
    # Unit Tests
    test_suite='nose2.collector.collector',
    tests_require=[
        'nose2',
        'nose2[coverage_plugin]>=0.6.5',
    ],
)
