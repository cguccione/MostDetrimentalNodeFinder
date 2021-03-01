#!/usr/bin/env python
import sys
import click
import igraph
from sortedcontainers import SortedDict


def damage(graph, source, sink, alpha=1):
    """
        return a final row of damges matrix 

        INPUTS: graph: an iGraph object ex. 0->1 1->2 2->3
                source: always equal to our 0 node
                sink: our target node
                alpha: adjustable value 

        VARIABLES:
                Influence: A priority queue(SortedDict): Node: influence
                Damage: Dictionary{}, key: Node, val: Priority Queue(SortedDict): Node: Damage

                ex. 1 -> 2 -> 3 
    """
    #print(graph.vcount()) #The number of vertices in the graph
    graph.vs['preColor'] = ['NA']*graph.vcount() #Adds a new attribute - pre-color to each NODE which tells us what the color of the edge from oldNode--Node is

    influence = SortedDict() #Initalize Influence- Priority Queue/Sorted Dict- Will hold Node:Damage

    ## first, initialize values for every unvisited node
    for v in graph.vs: #Loops through all list vertices in the graph
        #print(v) #Prints the entire node object, ex: igraph.Vertex(<igraph.Graph object at 0x7fa1a70cfc70>, 0, {})
        #print(v.index) #Prints just the node itself, ex: 0
        influence[v.index] = float('inf')

    influence[source] = 0 #Set the source node to 0

    print("Influence Priority Queue:", influence)

    ##run a modified Dijkstra's algorithm
    print("Source", source) #Currently source is just the number 0, or whatever node this corresponds to
    print("Source Object", graph.vs.find(source)) #This finds the igraph object related to source
    source = graph.vs.find(source)

    node = source #Node will hold our current node and starts with our source node-- This holds the igraph object
    while node != sink: #while sink is unvisited
        outEdges = node.out_edges() #Find all child nodes
        for i in outEdges: #Loop through all child nodes
            #print(i.target_vertex.index) #Just the node number
            #print(i.target_vertex) #The igraph object

            ##count the current edge
            influence[i.target_vertex.index] = influence[node.index] + 1

            ##check if the edge oldNode---node and node--new_node(i) are the same 'color'
            print("Attirbutes of Old Node--Node Edge, stored in Node", i.target_vertex.attributes())
            print("Attirbutes of Node--New Node Edge", i.attributes())
            Old2Node = i.target_vertex.attributes()['preColor'] #This works as a dictionary, so we must pull the 'preColor' object out of it
            Node2New = i.attributes()['type']
            print('OldNode--Node', Old2Node)
            print('Node--NewNode', Node2New)

            ### Can us te walkaround below instead-- if node != source: #If we have the source node, then we don't need to check the previous edge becuase it doesn't exist
            #First check to make sure that we are not at the source: NA, then if the edges still aren't equal then add alpha to influence
            if Old2Node != 'NA' and Old2Node != Node2New:
                influence[i.target_vertex.index] = influence[i.target_vertex.index] + alpha


            print("Influence Priority Queue:", influence)



        break




    damgeMatrix = {}


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

    
    #Testing igraph

    #print("-----------")
    #print("Graph", graph)
    #print("----")
    print("Graph Edges", graph.get_edgelist())
    print("Graph Type", graph.es['type'])
    """
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


@click.group()
@click.version_option()
def main():
    """
    Most Detrimental Node Finder\n
    Find the most detrimental node in a graph
    """
    pass


@main.command('sif')
@click.argument("fname")
@click.argument("source")
@click.argument("sink")
@click.argument("alpha", type=click.FLOAT, default=1)
def read_sif(fname, source, sink, alpha=1):
    """ Run the most detrimental node finder on an SIF file """
    # first import pandas and load the sif adjacency list into a dataframe
    import pandas as pd
    df = pd.read_csv(fname, sep = "\t", names = ["to","edge","from"])
    # convert to a graph
    graph = igraph.Graph.DataFrame(df[["to","from"]], directed = True)
    graph.es['type'] = df["edge"]
    # run the most detrimenal node finder
    node = most_detrimental(graph, source, sink, alpha)
    # output the most detrimental node
    click.echo('{}'.format(node))


if __name__ == "__main__":
    print(main(sys.argv[1]))
