#!/usr/bin/env python
import pytest
from igraph import Graph
from node_finder import most_detrimental, damage



def influence(path, alpha=1):
    """
        given a sequence of edge types (ie up, down), return the influence of the path
        consisting of those edges
        The influence is defined as |E| + alpha * (# of alternating colored edges)
    """
    return len(path) + alpha * sum(
        pair[0] != pair[1] for pair in zip(path[:-1], path[1:])
    )


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


# Check that the correct path is chosen when there are two possible paths, and one is
# just longer than the other

# GRAPH:
# 0->1 u
# 1->4 u
# 0->2 u
# 2->3 u
# 3->4 u

# SOURCE: 0
# SINK:   4

def test_two_paths_by_len():
    # create a graph with two possible paths to the source
    # where the best path is solely determined by length
    graph = Graph([(0,1), (1,4), (0,2), (2,3), (3,4)], directed=True)
    graph.es['type'] = ['up']*5

    # check that it chose the correct path by looking at the most damaging node
    node = most_detrimental(graph, 0, 4)
    assert node == 1

    # what are the influences of the two possible paths?
    influences = [influence(graph.es['type'][:2]), influence(graph.es['type'][2:])]

    # also check that it calculated the correct damages
    damages = damage(graph, 0, 4)
    assert damages.get(node, 0) == (influences[1]-influences[0])


# Check that the correct path is chosen when there are two possible paths, and one has
# more alternating edges

# GRAPH:
# 0->1 u
# 1->3 u
# 0->2 u
# 2->3 d

# SOURCE: 0
# SINK:   3

def test_two_paths_by_color():
    # create a graph with two possible paths to the source
    # where the best path is solely determined by the color
    graph = Graph([(0,1), (1,3), (0,2), (2,3)], directed=True)
    graph.es['type'] = ['up']*3 + ['down']

    node = most_detrimental(graph, 0, 3)
    assert node == 1

    # what are the influences of the two possible paths?
    influences = [influence(graph.es['type'][:2]), influence(graph.es['type'][2:])]

    # also check that it calculated the correct damages
    damages = damage(graph, 0, 3)
    assert damages.get(node, 0) == (influences[1]-influences[0])


# Check that the correct path is chosen when there are two possible paths, and one has
# more alternating edges and the other is longer

# GRAPH:
# 0->1 u
# 1->4 d
# 0->2 u
# 2->3 u
# 3->4 u

# SOURCE: 0
# SINK:   4

def test_two_paths_by_len_and_color():
    # create a graph with two possible paths to the source
    # where the best path isn't clear and depends on alpha
    graph = Graph([(0,1), (1,4), (0,2), (2,3), (3,4)], directed=True)
    graph.es['type'] = ['up', 'down', 'up', 'up', 'up']

    # case 1: alpha == 1 (the default)
    node = most_detrimental(graph, 0, 4)
    # any of the intermediate nodes could be most detrimental
    assert node in (1, 2, 3)

    # also check that it calculated the correct damages
    # they should all be the same (ie 0)
    damages = damage(graph, 0, 4)
    assert damages.get(1, 0) == 0
    assert damages.get(2, 0) == 0
    assert damages.get(3, 0) == 0

    # case 2: alpha == 1/2
    node = most_detrimental(graph, 0, 4, alpha=0.5)
    # the path that passes through node 1 is better
    assert node == 1

    # what are the influences of the two possible paths?
    influences = [influence(graph.es['type'][:2], alpha=0.5), influence(graph.es['type'][2:], alpha=0.5)]
    # also check that it calculated the correct damages
    damages = damage(graph, 0, 4, alpha=0.5)
    assert damages.get(node, 0) == (influences[1]-influences[0])

    # case 3: alpha == 2
    node = most_detrimental(graph, 0, 4, alpha=2)
    # the path that passes through nodes 2 and 3 is better
    assert node in (2, 3)

    # what are the influences of the two possible paths?
    influences = [influence(graph.es['type'][:2], alpha=2), influence(graph.es['type'][2:], alpha=2)]
    # also check that it calculated the correct damages
    damages = damage(graph, 0, 4, alpha=2)
    assert damages.get(node, 0) == (influences[0]-influences[1])


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
