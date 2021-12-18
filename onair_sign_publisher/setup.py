import os
from setuptools import find_packages, setup
from setuptools.command.install import install
import PyInstaller.__main__
import shutil

NAME = 'onair_sign_publisher'
VERSION = '0.0.1'


class PyinstallerCommand(install):

    OUTPUT_DIR = f'dist/{NAME}_{VERSION}'
    ARCHIVE_NAME = f'{NAME}_{VERSION}'

    def run(self):
        shutil.rmtree(self.OUTPUT_DIR, ignore_errors=True)
        PyInstaller.__main__.run([
            'onair_sign_publisher/publisher.py',
            '--paths', 'onair_sign_publisher',
            '--distpath', self.OUTPUT_DIR,
            '--specpath', 'build/',
            '--onefile'
        ])
        shutil.copy('config.json', self.OUTPUT_DIR + '/config.json')
        shutil.make_archive(
            'dist/' + self.ARCHIVE_NAME,
            'zip',
            root_dir='dist/',
            base_dir=f'{NAME}_{VERSION}',
        )


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name=NAME,
    version=VERSION,
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