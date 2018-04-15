from setuptools import setup

setup(
    name='Vimcryption',
    version='0.1',
    description='Test package for VIMCryption VIM plugin.',
    author='Tom Manner, Miguel Nistal',
    author_email='tom.s.manner@gmail.com, nistam328@gmail.com',
    url='https://www.github.com/tsmanner/vimcryption',
    packages=[
        'plugin',
    ],
    install_requires=[
        'nose2',
    ],
)
