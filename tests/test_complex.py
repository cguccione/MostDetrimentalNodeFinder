#!/usr/bin/env python
import pytest
from igraph import Graph
from node_finder import most_detrimental, damage


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
    # create a more complicated graph:
    # All 3 paths must pass through node 1, the first internal node (after the source)
    graph = Graph([(0,1), (1,3), (3,2), (1,2), (1,4), (2,5), (4,5)], directed=True)
    graph.es['type'] = ['up', 'up', 'down', 'down', 'down', 'up', 'down']

    node = most_detrimental(graph, 0, 5)
    assert node == 1

    # also check that the damage comes out to infinity, as desired
    damages = damage(graph, 0, 5)
    assert damages[node] == float('inf')

    # check that the damage of node 4 is 1, since the path that passes through node 4
    # is the best one and has influence 4 but there's two more that both have an
    # influence of 5:
    # 5-4 = 1
    assert damages[4] == 1


# In this graph, any of the nodes could be the most damaging! All should have damage 0
# because there is an alternate path that doesn't include them

# GRAPH:
# 0->1 u
# 0->2 u
# 2->3 d
# 1->3 d
# 1->4 d
# 3->5 u
# 4->5 d

# SOURCE: 0
# SINK:   5

def test_infinity():
    graph = Graph([(0,1), (0,2), (2,3), (1,3), (1,4), (3,5), (4,5)], directed=True)
    graph.es['type'] = ['up', 'up', 'down', 'down', 'down', 'up', 'down']

    node = most_detrimental(graph, 0, 5)
    assert node in (1, 2, 3, 4)

    # also check that each node's damage comes out to 0, as desired
    damages = damage(graph, 0, 5)
    for node in (1, 2, 3, 4):
        assert damages[node] == 0
