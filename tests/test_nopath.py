#!/usr/bin/env python
import pytest
from igraph import Graph
from node_finder import most_detrimental


# Do we output None if there is no path between source and sink?


# GRAPH:
# 0->1 u
# 2->1 u

# SOURCE: 0
# SINK:   2

def test_directions():
    # create a graph consisting of three nodes
    # where the other two nodes are pointing towards the middle one:
    # 0->1<-2
    graph = Graph([(0,1), (2,1)], directed=True)
    graph.es['type'] = ['up', 'up']

    node = most_detrimental(graph, 0, 2)
    assert node is None


# GRAPH:
# 0->1 u
# 2->3 u

# SOURCE: 0
# SINK:   3

def test_not_connected():
    # create a graph with two unconnected edges
    graph = Graph([(0,1), (2,3)], directed=True)
    graph.es['type'] = ['up', 'up']

    node = most_detrimental(graph, 0, 3)
    assert node is None
