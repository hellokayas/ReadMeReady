"""Python setup.py for doc_generator package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("doc_generator", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="doc_generator",
    version=read("doc_generator", "VERSION"),
    description="Generate code documentation in Markdown format in seconds.",
    url="https://github.com/souradipp76/doc_generator/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="souradipp76",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["doc_generator = doc_generator.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
