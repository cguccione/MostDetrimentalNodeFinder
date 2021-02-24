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


# Same graph. But this time, there's an extra edge from node 0 to node 2. There are
# two possible paths to the sink, so this will test if the correct path was chosen.
# The path that directly connects node 0 with node 1 should be chosen over the path
# that first passes through the intermediate node 2

# GRAPH:
# 0->1 u
# 2->1 u
# 0->2 u

# SOURCE: 0
# SINK:   1

def test_two_paths_no_node():
    # create a graph consisting of three nodes
    # where the other two nodes are pointing towards the middle one:
    # 0->1<-2
    graph = Graph([(0,1), (2,1), (0,2)], directed=True)
    graph.es['type'] = ['up']*3

    node = most_detrimental(graph, 0, 1)
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
