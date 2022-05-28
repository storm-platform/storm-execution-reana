# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-runner-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Plugin for the Storm Runner to enable experiments execution on REANA instances."""

import os

from setuptools import find_packages, setup

readme = open("README.rst").read()
history = open("CHANGES.rst").read()

tests_require = []

extras_require = {
    "docs": [
        "Sphinx>=3,<4",
    ],
    "tests": tests_require,
}

extras_require["all"] = [req for _, reqs in extras_require.items() for req in reqs]

setup_requires = []

install_requires = [
    # General
    "pydash>=5.1.0,<6.0",
    "docker>=5.0.3,<6.0",
    # Reana
    "reana-client @ git+https://github.com/storm-platform/tp-reana-client@master",
    "reana-commons[yadage,snakemake] @ git+https://github.com/storm-platform/tp-reana-commons@master",
    # Storm
    "storm-runner @ git+https://github.com/storm-platform/storm-runner@main",
    "storm-reprozip-proxy @ git+https://github.com/storm-platform/storm-reprozip-proxy@main",
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join("storm_runner_reana", "version.py"), "rt") as fp:
    exec(fp.read(), g)
    version = g["__version__"]

setup(
    name="storm-runner-reana",
    version=version,
    description=__doc__,
    long_description=readme + "\n\n" + history,
    keywords=[
        "Utility",
        "Reproducible Research",
        "ReproZip",
        "Reana",
        "Storm Platform",
    ],
    license="MIT",
    author="Felipe Menino Carlos",
    author_email="felipe.carlos@inpe.br",
    url="https://github.com/storm-platform/storm-runner-reana",
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    entry_points={
        "storm_runner.plugins": [
            "storm-runner-reana-reprozip = storm_runner_reana:StormRunnerReana"
        ],
        "invenio_db.models": [
            "storm_runner_reana_docker = storm_runner_reana.environment.docker"
        ],
        "invenio_celery.tasks": [
            "storm_runner_reana_reprozip_serial = storm_runner_reana.contrib.reprozip.services.serial.tasks",
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 1 - Planning",
    ],
)
