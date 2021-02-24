#!/usr/bin/env python
import pytest
from igraph import Graph
from node_finder import most_detrimental


# Run the simple example provided in our README:
# A graph consisting of three sequential nodes where the most detrimental node should
# be the one in the middle

# GRAPH:
# A->B
# B->C

# SOURCE: A
# SINK:   C

def test_example():
	graph = Graph.Formula('A->B->C')
	node = most_detrimental(graph, 'A', 'C')
	assert node == 'B'
