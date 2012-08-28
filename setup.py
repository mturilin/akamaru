import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
akamaru_dir = 'akamaru'

for dirpath, dirnames, filenames in os.walk(akamaru_dir):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(
    name = "akamaru",
    version = "2.0.1",
    author = "Mikhail Turilin",
    author_email = "mturilin@gmail.com",
    description = ("Very simple social auth backend for Django "),
    license = "BSD",
    keywords = "django social auth google facebook trello vkontakte",
    url = "https://github.com/mturilin/akamaru",
    packages = packages,
    data_files = data_files,
    long_description=read('README.md'),
    include_package_data = True,
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