#!/usr/bin/env python

from setuptools import setup

setup(
    name="VigoBusAPI",
    version="0.1.0",
    description="Python + Flask API that provide Stop and Bus information provided by the public transport system "
                "of the city of Vigo (Galicia/Spain)",
    long_description="Intermediate Python + Flask API that provide Stop and Bus information provided by the public "
                     "transport system of the city of Vigo (Galicia/Spain). The goal of this API is to keep the "
                     "different data sources and APIs available on one single API with better endpoints structure "
                     "and more clear data output format (as JSON).",
    author="David Lorenzo",
    url="https://github.com/David-Lor/Python_VigoBusAPI",
    packages=("vigobusapi",),
    install_requires=(
        "zeep",
        "flask",
        "requests-html",
        "beautifulsoup4",
        "roman",
        "gevent",
        "timeout-decorator",
        "python-dotenv",
        "pybuses",
    ),
    dependency_links=(
        "git+https://github.com/David-Lor/PyBuses.git#egg=pybuses",
    ),
    entry_points={
            'console_scripts': ['vigobusapi=vigobusapi:run'],
    },
)
