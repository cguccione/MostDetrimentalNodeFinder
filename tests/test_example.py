#!/usr/bin/env python
import pytest
from igraph import Graph
from node_finder import most_detrimental


# Run the simple example provided in our README:
# A graph consisting of three sequential nodes where the most detrimental node should
# be the one in the middle

# GRAPH:
# A->B u
# B->C u

# SOURCE: A
# SINK:   C

def test_example():
    # create a graph consisting of three nodes connected in sequence
    # every edge will be upregulating
    graph = Graph.Formula('A->B->C')
    graph.es['type'] = ['up']*2
    # the most detrimental node should be B
    node = most_detrimental(graph, 'A', 'C')
    assert node == 'B'


# The contents of the 'type' attribute should probably be irrelevant. Our
# implementation should just check whether they are equal, not that they equal a
# specific, expected value. In other words, it should be agnostic of this input

# GRAPH:
# A->B u
# B->C u

# SOURCE: A
# SINK:   C

def test_example_other_types():
    for edge_types in (('up', 'down'), (0, 1), ('activates', 'inactivates'), (100, -200)):
        # create a graph consisting of three nodes connected in sequence
        # every edge will be upregulating
        graph = Graph.Formula('A->B->C')
        graph.es['type'] = edge_types
        # the most detrimental node should be B
        node = most_detrimental(graph, 'A', 'C')
        assert node == 'B', 'Failed with edge types {} and {}'.format(*edge_types)
