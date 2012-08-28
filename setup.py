import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "akamaru",
    version = "2.0.1",
    author = "Mikhail Turilin",
    author_email = "mturilin@gmail.com",
    description = ("Very simple social auth backend for Django "),
    license = "BSD",
    keywords = "django social auth google facebook trello vkontakte",
    url = "https://github.com/mturilin/akamaru",
    packages = find_packages(),
    include_package_data = True,
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
        'path.py',
        'requests',
        'oauthlib',
    ]
)