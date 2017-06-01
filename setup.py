# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from os import path
import subprocess

here = path.abspath(path.dirname(__file__))

# Try to create an rst long_description from README.md
try:
    args = 'pandoc', '--to', 'rst', 'README.md'
    long_description = subprocess.check_output(args)
    long_description = long_description.decode()
except Exception as error:
    print('README.md conversion to reStructuredText failed. Error:')
    print(error)
    print('Setting long_description to None.')
    long_description = None

setup(
    name='obt',
    version='0.1.0',
    description='A Python library for The Oslo-Bergen Tagger',
    long_description=long_description,
    url='https://github.com/draperunner/obt',
    author='Mats Byrkjeland',
    author_email='matsbyr@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='pos-tagging nlp pos',
    #packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    py_modules=["obt"],
    install_requires=[],
    extras_require={
        'dev': [],
        'test': [],
    },
    package_data={},
    entry_points={
        'console_scripts': [],
    },
)
