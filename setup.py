from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='node_finder',
    version='0.0.1',
    description="Find a node that, when removed, will cause the most damage to a shortest path between two vertices in a directed graph",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cguccione/MostDetrimentalNodeFinder",
    install_requires=[
        'python-igraph',
        'pytest'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(include=['node_finder'])
)
