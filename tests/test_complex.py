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

    # the damages of nodes 2 and 3 should be 0, since the most influential path doesn't
    # pass through those nodes
    assert damages[2] == 0
    assert damages[3] == 0


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

def test_all_same_damages():
    graph = Graph([(0,1), (0,2), (2,3), (1,3), (1,4), (3,5), (4,5)], directed=True)
    graph.es['type'] = ['up', 'up', 'down', 'down', 'down', 'up', 'down']

    node = most_detrimental(graph, 0, 5)
    assert node in (1, 2, 3, 4)

    # also check that each node's damage comes out to 0, as desired
    damages = damage(graph, 0, 5)
    for node in (1, 2, 3, 4):
        assert damages[node] == 0


# This graph helps test whether our code works for bowtie-like graphs, where two paths
# merge and then separate from each other again before finally converging on the sink.
# But before we test the botwie, we try the pincer, where the two paths simply converge
# without crossing.

# GRAPH:
# 0->1 d
# 1->2 u
# 2->3 d
# 0->4 d
# 4->5 d
# 5->6 d
# 6->3 d
# 3->7 d
# 7->8 d
# 8->9 d
# 7->10 u
# 10->9 d

# SOURCE: 0
# SINK:   7, 9

def test_bowtie():
    # This graph has two paths that split from the source and then converge on node 3.
    # The first of the two paths consists of three alternating edges and the second
    # path consists of four non-alternating edges.
    # There's a single edge from node 3 to node 7 and then there are two paths (each of
    # length: 2 edges) that split out from node 7 before converging again on node 9.
    # One of the final two paths has alternating edges while the other does not.
    graph = Graph([
        (0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (5, 6), (6, 3), (3, 7), (7, 8), (8, 9),
        (7, 10), (10, 9)
    ], directed=True)
    graph.es['type'] = [
        'down', 'up', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down',
        'up', 'down'
    ]

    # first, try the pincer
    node = most_detrimental(graph, 0, 7)
    assert node == 3

    # also check that the most damage comes out to infinity, as desired
    damages = damage(graph, 0, 7)
    assert damages[node] == float('inf')

    # check that the damages of nodes 4, 5, and 6 is 1 since the best path passes
    # through those nodes and it has an influence of 4, whereas the next best path has
    # an influence of 5 (because it alternates colors, even though it is shorter)
    # 5-4 = 1
    assert damages[4] == 1
    assert damages[5] == 1
    assert daamges[6] == 1

    # the damage of the other nodes should be 0, since the most influential path
    # doesn't pass through them
    assert damages[1] == 0
    assert damages[2] == 0

    # now, let's try the bowtie!
    node = most_detrimental(graph, 0, 9)
    assert node in (3, 7)

    # also check that the most damage comes out to infinity, as desired
    damages = damage(graph, 0, 9)
    assert damages[7] == float('inf')

    # check that the damages of node 8 is 1 since the best path passes
    # through that node and it has a total influence of 7, whereas the next best path
    # has an influence of 8 (because it has one alternating node)
    # 8-7 = 1
    assert damages[8] == 1

    # the damage of the other node should be 0, since the most influential path
    # doesn't pass it
    assert damages[10] == 0

    # just in case, assert that the damages of the other nodes haven't changed
    assert damages[1] == 0
    assert damages[2] == 0
    assert damages[3] == float('inf')
    assert damages[4] == 1
    assert damages[5] == 1
    assert daamges[6] == 1


# This graph helps test whether our code works for cycles.
# Cycles should never appear in a most influential path because they always extend the
# length of the path and (potentially) the number of alternating edges.

# GRAPH:
# 0->1 u
# 1->2 u
# 2->3 u
# 2->4 u
# 4->1 u

# SOURCE: 0
# SINK:   3

def test_cycle():
    # This graph consists of four consecutive nodes 0, 1, 2, and 3 and one more extra
    # node 4. A cycle begins at node 2, passes through node 4, and then ends at node 1.
    # All edges have the same color.
    graph = Graph([(0, 1), (1, 2), (2, 3), (2, 4), (4, 1)], directed=True)
    graph.es['type'] = ['up']*5

    # for all values of alpha, the results should be the same
    # so let's test a bunch of them
    for alpha in (1, 2, 100, 0.5, 0.1):
        # Nodes 1 and 2 will be the most detrimental because they are the internal nodes
        # within the path that connects source to sink. The presence of the cycle does
        # not change the fact that they are absolutely required.
        node = most_detrimental(graph, 0, 3, alpha)
        assert node in (1, 2)

        # also check that the most damage comes out to infinity, as desired
        damages = damage(graph, 0, 3, alpha)
        assert damages[1] == float('inf')
        assert damages[2] == float('inf')

        # and check that the damage of node 4 is 0, since the most influential path
        # should not pass through it!
        assert damages[4] == 0
