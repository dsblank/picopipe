# -*- coding: utf-8 -*-

import io
import os

import setuptools

name = "picopipe"

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md"), "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name=name,
    version="1.0.0",
    url="https://github.com/dsblank/%s" % name,
    author="Douglas Blank",
    description="A small pipeline framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
    ],
    packages=[],
    python_requires=">=3.9",
    license="Apache 2.0",
    platforms="Linux, Mac OS X, Windows",
    keywords=["machine learning", "artificial intelligence", "pipelines",
              "python", "data science"],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

if __name__ == "__main__":
    setuptools.setup(**setup_args)
