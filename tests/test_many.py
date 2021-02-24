#!/usr/bin/env python
import pytest
from igraph import Graph
from node_finder import most_detrimental


# Ensure that we correctly handle cases where the damage is infinite
# In this graph, node 1 sits between every path from source to sink

# GRAPH:
# 0->1 u
# 1->3 u
# 3->2 d
# 1->2 d
# 1->4 d
# 2->5 u
# 4->5 d

# SOURCE: 0
# SINK:   5

def test_infinity():
    # create a more complicated graph
    graph = Graph([(0,1), (1,3), (3,2), (1,2), (1,4), (2,5), (4,5)], directed=True)
    graph.es['type'] = ['up', 'up', 'down', 'down', 'down', 'up', 'down']

    node = most_detrimental(graph, 0, 5)
    assert node == 1
