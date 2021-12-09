import os
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="onair_sign_publisher",
    version="0.0.1",
    author="Torsten Wylegala",
    author_email="mail@twyleg.de",
    description=("Publisher for on air sign (camera and microphone state are published)"),
    license="GPL 3.0",
    keywords="onair sign",
    url="https://github.com/twyleg/onair_sign",
    packages=find_packages(),
    long_description=read('README.md'),
    install_requires=[
        'requests'
    ]
)