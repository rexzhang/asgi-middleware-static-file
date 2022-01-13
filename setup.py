#!/usr/bin/env python
# coding=utf-8

# Template:
# https://github.com/rexzhang/pypi-package-project-template/blob/master/setup.py

from typing import List

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from pathlib import Path

import asgi_middleware_static_file as module

root_path = Path(__file__).parent
requirements_path = root_path.joinpath("requirements")

# Get the long description from the README file
with open(root_path.joinpath("README.md").as_posix(), encoding="utf-8") as f:
    long_description = f.read()


# Get install_requires from requirements.txt
def _read_requires_from_requirements_txt(
    base_path: Path, filename: str, ignore_base: bool = False
) -> List[str]:
    _requires = []
    with open(base_path.joinpath(filename).as_posix(), encoding="utf-8") as req_f:
        lines = req_f.readlines()
        for line in lines:
            if line == "\n" or line == "" or line[0] == "#":
                continue

            words = line.rstrip("\n").split(" ")
            if words[0] == "-r":
                if ignore_base and words[1] == "base.txt":
                    continue

                else:
                    _requires.extend(
                        _read_requires_from_requirements_txt(
                            base_path=base_path, filename=words[1]
                        )
                    )

            else:
                _requires.append(words[0])

    return _requires


install_requires = _read_requires_from_requirements_txt(
    base_path=requirements_path, filename="base.txt"
)
extras_require_dev = list(
    set(
        _read_requires_from_requirements_txt(
            base_path=requirements_path, filename="dev.txt"
        )
    )
)

# Setup
setup(
    name="ASGIMiddlewareStaticFile",
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=module.__version__,
    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    description=module.__description__,  # Optional
    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    #
    # Often, this is the same as your README, so you can just read it in from
    # that file directly (as we have already done above)
    #
    # This field corresponds to the "Description" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=long_description,  # Optional
    # Denotes that our long_description is in Markdown; valid values are
    # text/plain, text/x-rst, and text/markdown
    #
    # Optional if long_description is written in reStructuredText (rst) but
    # required for plain-text or Markdown; if unspecified, "applications should
    # attempt to render [the long_description] as text/x-rst; charset=UTF-8 and
    # fall back to text/plain if it is not valid rst" (see link below)
    #
    # This field corresponds to the "Description-Content-Type" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    # The project's main homepage.
    url=module.__project_url__,
    # Author details
    author=module.__author__,
    author_email=module.__author_email__,
    # Choose your license
    license=module.__licence__,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    # What does your project relate to?
    keywords="asgi middleware staticfile asycnio",
    py_modules=["asgi_middleware_static_file"],
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=install_requires,
    python_requires=">=3.5",
    # extras_require={},
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={
    #     'console_scripts': [
    #         '',
    #     ],
    # },
)
