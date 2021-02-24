# MostDetrimentalNodeFinder
Find a node that, when removed, will cause the most damage to a shortest path between two vertices in a directed graph

## Installation
For development:
```
git clone https://github.com/cguccione/MostDetrimentalNodeFinder
pip install -e MostDetrimentalNodeFinder
```

## Usage
Our code utilizes the `python-igraph` library for graph representation. You must first create a graph with that library before executing our code.
```
import node_finder
from igraph import Graph

# create a graph consisting of three nodes connected in sequence
graph = Graph.Formula('A->B->C')
# each edge must have a type: up (for upgregulating) or down( for downregulating)
graph.es['type'] = ['up']*2

# should return 'B'
node_finder.most_detrimental(graph, source='A', sink='C')
```

## Executing tests
To run all of our tests:
```
py.test tests/
```
