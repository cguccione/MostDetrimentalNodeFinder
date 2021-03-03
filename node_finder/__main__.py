#!/usr/bin/env python
import sys
import click
import igraph
from sortedcontainers import SortedDict
from collections import defaultdict


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

    influence = SortedDict() #Initalize Influence- Priority Queue/Sorted Dict- Will hold Node: Influence
    Damage = defaultdict(SortedDict) #Initalize Damage- Dictionary of: Priority Queue/Sorted Dic- Will hold: Node [Node] = Damge

    ## first, initialize values for every unvisited node
    for v in graph.vs: #Loops through all list vertices in the graph
        #print(v) #Prints the entire node object, ex: igraph.Vertex(<igraph.Graph object at 0x7fa1a70cfc70>, 0, {})
        #print(v.index) #Prints just the node itself, ex: 0
        influence[v.index] = float('inf')
        Damage[v.index][v.index] = float('inf')

    influence[source] = 0 #Set the source node to 0
    Damage[source] = SortedDict()

    print("Influence Priority Queue:", influence)
    print()

    ##run a modified Dijkstra's algorithm
    #print("Source", source) #Currently source is just the number 0, or whatever node this corresponds to
    #print("Source Object", graph.vs.find(source)) #This finds the igraph object related to source
    source = graph.vs.find(source)

    vistedNodes=[] #The index(number only) of all nodes which have already been visited
    
    ####bestPath= defaultdict(list) #Key: node,  Def:List of nodes on best path between source and node - not including source or child
    ####bestPath[0] #{0:[]} 
    ####print ("BEST", bestPath)

    node = source #Node will hold our current node and starts with our source node-- This holds the igraph object
    while node.index != sink: #while sink is unvisited
        outEdges = node.out_edges() #Find all child nodes
        for i in outEdges: #Loop through all child nodes
            #print(i.target_vertex.index) #Just the node number
            #print(i.target_vertex) #The igraph object

            ##count the current edge
            newInfluence = influence[node.index] + 1

            ##check if the edge oldNode---node and node--new_node(i) are the same 'color'
            print("Attirbutes of Old Node--Node Edge, stored in Node", i.target_vertex.attributes())
            print("Attirbutes of Node--New Node Edge", i.attributes())
            Old2Node = i.target_vertex.attributes()['preColor'] #This works as a dictionary, so we must pull the 'preColor' object out of it
            Node2New = i.attributes()['type']
            print('OldNode--Node', Old2Node)
            print('Node--NewNode', Node2New)
            print()

            ### Can us te walkaround below instead-- if node != source: #If we have the source node, then we don't need to check the previous edge becuase it doesn't exist
            #First check to make sure that we are not at the source: NA, then if the edges still aren't equal then add alpha to influence
            if Old2Node != 'NA' and Old2Node != Node2New:
                newInfluence = newInfluence + alpha

            '''
            ##Update inflence function
            if influence[i.target_vertex.index] > newInfluence: #If we want to take this path?
               influence[i.target_vertex.index] = newInfluence
               #Update best path
               bestPath[node.index].append(i.target_vertex.index)
            '''

            ##update the damages stored in the child
            #for other in Damage[node.index]: # for every node other on the best path between source and child:

            #####currentNodeBestPath = bestPath[node.index] ###Should this be i.target_vertex.index ???
            #This contains just node numbers, not igraph objects

            #####for other in currentNodeBestPath:

            if influence[i.target_vertex.index] > newInfluence: #If we are on the best path
                Damage[i.target_vertex.index].update(Damage[node.index]) #Copies all values from node.index into child.inex
            #Ensures that the sorted dictionarires will contain the nodes of the best path from source(not included) to node

            else:
                #for other in Damage[node.index].keys():
                for other in Damage[i.target_vertex.index].keys():
                    print("Node", node.index)
                    print("Child", i.target_vertex.index)
                    print("Other", other)
                    #if other not in Damage[node.index]:
                    if other in Damage[node.index] and Damage[node.index][other] == float('inf'):
                        new_damge = float('inf')
                    else:
                        new_damge = newInfluence - influence[i.target_vertex.index]
                        print("------------------------------------------")
                        print("newInfluence", newInfluence)
                        print("Infludnce Child", influence[i.target_vertex.index])
                        print("New Damage", new_damge)
                    ##Update Damage
                    if other in Damage[i.target_vertex.index]:
                        current_damge = Damage[i.target_vertex.index][other]
                        final_damage = min(current_damge, new_damge)
                        Damage[i.target_vertex.index][other] = final_damage
                    else:
                        Damage[i.target_vertex.index][other] = new_damge
            
            
            ##Update inflence function
            if influence[i.target_vertex.index] > newInfluence: #If we want to take this path?
               influence[i.target_vertex.index] = newInfluence
               
               #Update best path
               #####bestPath[node.index].append(i.target_vertex.index) 
            

            #Updating the preColor for the current  --- Should this be outside the loop?
            #print("Check vertex", i.target_vertex)
            i.target_vertex['preColor'] = str(Node2New)
            #print("Check vertex", i.target_vertex)

            print("Influence Priority Queue:", influence)
            print("Damges", Damage)


        ##Add current node to the visted Nodes
        vistedNodes.append(node.index)
        print("vistedNodes", vistedNodes)
        print("")

        #an unvisited node with the smallest influence from source
        for Node, infVal in influence.items(): #Loops through infuence priority queue in order- should be shorted
            #print(Node, infVal)#Node and correspoinding value -- These should be in order based on value
            if Node not in vistedNodes: #Once we hit something that is not in vistedNodes, then this is the smallest inflence that hasn't been visited as desired
                node = graph.vs.find(Node)
                #print("node", node)
                break
    
    del Damage[sink][sink]

    ##Check Point
    print("----------------------------------------------------------------------------")
    print("Final Node: ", node.index)
    print("Influence Priority Queue:", influence)
    print("Damage:", Damage)

    return Damage[sink]

def most_detrimental(graph, source, sink, alpha=1):
    """
        return a node that, when removed, will cause the most damage to a shortest path
        between source and sink in the directed graph
    """
    print("Graph Edges", graph.get_edgelist())
    print("Graph Type", graph.es['type'])
    print()

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
