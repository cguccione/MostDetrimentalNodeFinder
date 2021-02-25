#!/usr/bin/env python
import igraph
from sortedcontainers import SortedDict

def damage(graph, source, sink, alpha=1):
    """
        return a final row of damges matrix 

    """

    sd = SortedDict({'A': 1, 'B': 3}) #Sorts based upon the value
    return sd
    #return damages

def most_detrimental(graph, source, sink, alpha=1):
    """
        return a node that, when removed, will cause the most damage to a shortest path
        between source and sink in the directed graph

        Variables:
        influence
    """

    """
    Testing igraph

    print("-----------")
    print("Graph", graph)
    print("----")
    print("Graph Edges", graph.get_edgelist())
    print("Graph Type", graph.es['type'])
    print("Input: name of the node, Ouput node as an object", graph.vs.find(source))
    node = graph.vs.find(source)
    print("Finds all edges going out of the node: Gives a list of edges", node.out_edges())
    outEdges = node.out_edges()

    for edge in graph.get_edgelist():
        print(edge)

    print ("-----------")
    for i in outEdges:
        print(i.attributes()) #Edges attributes
        #Target node is the the node that the current edge is pointing to 
        print(i.target_vertex) #Gives the node object
        print(i.target_vertex.attributes()) #Give the attributes of the nodes (for our case we don't have this)
        print(i.target_vertex.index) #Gives the node itself again - finds index on the node
        print(i.target) #Gives the node itself
    """

    damages = damage(graph, source, sink, alpha=1) 
    #Damges = priority queue (SortedDict object): only has the sink node ('one-column'), 
    #{sink:{"node1": "damage of removing node1 in path from source to sink", "node2: "....""}}

    return damages.peekitem(index = -1)[0] #Finding the maximum node from the priority queue  Damages
