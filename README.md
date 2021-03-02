# MostDetrimentalNodeFinder
Find a node that, when removed, will cause the most damage to a shortest path between two vertices in a directed graph

## Installation
For development:
```
git clone https://github.com/cguccione/MostDetrimentalNodeFinder
cd MostDetrimentalNodeFinder
pip install -e '.[test]'
```

## Usage
### Via our python module
Our code utilizes the `python-igraph` library for graph representation. You must first create a graph with that library before executing our code.
```
import node_finder
from igraph import Graph

# create a graph consisting of three nodes connected in sequence
graph = Graph.Formula('A->B->C')
# each edge must have a type: 'up' (for upgregulating) or 'down' (for downregulating)
# each edge represents an upregulating relationship, in this case
graph.es['type'] = ['up']*2

# should return 'B'
node_finder.most_detrimental(graph, source='A', sink='C')
```
### Directly from the terminal
We also offer a command line utility, `nodefinder`, for ease of use.
```
$ nodefinder --help
Usage: nodefinder [OPTIONS] COMMAND [ARGS]...

  Most Detrimental Node Finder

  Find the most detrimental node in a graph

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  sif  Run the most detrimental node finder on an SIF file
```

## Executing tests
To run all of our tests:
```
py.test tests/
```
