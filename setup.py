from setuptools import setup, find_packages


setup(
    name="akamaru",
    version="2.0.15",
    author="Mikhail Turilin",
    author_email="mturilin@gmail.com",
    description='Very simple social auth backend for Django ',
    license='MIT',
    url="https://github.com/mturilin/akamaru",
    long_description="Very simple social auth backend for Django ",
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        'path.py',
        'requests',
        'oauthlib',
    ],

)
