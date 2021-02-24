#!/usr/bin/env python
import pytest
from igraph import Graph
from node_finder import most_detrimental


# A graph with a single edge doesn't have a most damaging node. Let's check if that
# case is handled

# GRAPH:
# 0->1 u

# SOURCE: 0
# SINK:   1

def test_single_edge():
    # create a graph consisting of a single edge
    graph = Graph([(0,1)], directed=True)
    graph.es['type'] = ['up']

    node = most_detrimental(graph, 0, 1)
    assert node is None


# If there are two possible, equally damaging nodes, either can be chosen.

# GRAPH:
# 0->1 u
# 1->2 u
# 2->3 u

# SOURCE: 0
# SINK:   3

def test_two_options():
    # create a graph consisting of four nodes connected in sequence
    graph = Graph([(0,1), (1,2), (2,3)], directed=True)
    graph.es['type'] = ['up']*3

    node = most_detrimental(graph, 0, 3)
    assert node in (1, 2)


# Check that the code can correctly ignore stray edges that can't be reached from the
# source node

# GRAPH:
# 0->1 u
# 1->2 u
# 3->2 u

# SOURCE: 0
# SINK:   2

def test_stray_edge_sink():
    # create a graph consisting of three nodes connected in sequence, plus an extra
    # edge pointing to the sink
    graph = Graph([(0,1), (1,2), (3,2)], directed=True)
    graph.es['type'] = ['up']*3

    node = most_detrimental(graph, 0, 2)
    assert node == 1


# Also test edges that, when followed, never reach the sink

# GRAPH:
# 0->1 u
# 1->2 u
# 0->3 u

# SOURCE: 0
# SINK:   2

def test_stray_edge_source():
    # create a graph consisting of three nodes connected in sequence, plus an extra
    # edge pointing out from the source
    graph = Graph([(0,1), (1,2), (0,3)], directed=True)
    graph.es['type'] = ['up']*3

    node = most_detrimental(graph, 0, 2)
    assert node == 1
