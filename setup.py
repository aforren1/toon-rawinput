from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# description for pypi
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    desc = f.read()

setup(
    name='toon_rawinput',
    version='0.0.1',
    description='Tools for neuroscience experiments',
    long_description=desc,
    long_description_content_type='text/markdown',
    url='https://github.com/aforren1/toon',
    author='Alexander Forrence',
    author_email='aforren1@jhu.edu',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    keywords='',
    packages=find_packages(exclude=['demo', 'benchmarks', 'teensy', 'scratch'])
)