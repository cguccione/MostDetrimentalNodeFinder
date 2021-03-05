#!/usr/bin/env python
import sys
import click
import igraph
from pqdict import pqdict
from collections import defaultdict, ChainMap

def damage_at_child(old_child_damage, new_child_damage, old_influence, new_influence, child):
    '''Inputs:
    old_child_damage: Priority Queue (sorted Dict) {{1:2}, {3:2}}
    new_child_damage: Priority Queue (sorted Dict)
    old_influence : Influence currently at the child
    new_influence : Possibly better influence at the child
    child: index of the child

    -Consturcts a new prioroty queue which represents the damages at the child
    -Constructs from either the old or new priority queue
    '''
    if old_influence > new_influence: #Replace the damages completley
        new_damage = old_influence - new_influence
        print("---")
        print("Old Inf", old_influence)
        print("New Inf", new_influence)
        print("NEW DAMAGA P1", new_damage)
        child_damage = new_child_damage.copy()
        for node, damage in new_child_damage.items(): #new_child_damage -- shoudln't contain itself (the child)
            #child_damage[node]=min(new_damage, damage, old_child_damage.get(node, float('inf')))
            if node in old_child_damage: #Will be true if we have alread touched this child ## True for node 1 but not node 4
                #child_damage[node]=min(damage, old_child_damage.get(node, float('inf')))
                updated_damage = old_child_damage[node] + new_damage
                # child_damage[node]=min(damage, old_child_damage[node])
            else:
                print("Are we hitting line 28")
                #child_damage[node]=min(new_damage, damage, old_child_damage.get(node, float('inf')))
                #child_damage[node]=min(new_damage, damage, old_child_damage.get(node, float('inf')))
                print("NEW DAMAGA", new_damage)
                updated_damage = new_damage
            child_damage[node] = min(damage, updated_damage)

    else: #Updating the old damages
        new_damage = new_influence - old_influence
        child_damage = old_child_damage
        for node, damage in old_child_damage.items():

            # child_damage[node]=min(new_damage, damage)

            if node in new_child_damage: #Already have a damage- 
                print("ENTERING======================================================================! :)")
                print("new_child_damage[node]", new_child_damage[node])
                print("new_damage", new_damage)
                print("---")
                #new_child_damage[node] - new_influence + old_influence
                """
                if new_child_damage[node] < new_damage:
                    NEW_damage = new_child_damage[node]
                else:
                    NEW_damage = new_child_damage[node] - new_damage
                """
                #A#NEW_damage = new_child_damage[node] - new_damage
                updated_damage = new_child_damage[node] + new_damage
                print("NEW", updated_damage)
                print("damage", damage)
            else:
                updated_damage = new_damage
            child_damage[node] = min(damage, updated_damage)
                #green - pink           - green         + yellow

    child_damage[child] = float("inf")
    return child_damage


def damage(graph, source, sink, alpha=1, also_return_visited=False):
    """
        return a final row of damges matrix 

        INPUTS: graph: an iGraph object ex. 0->1 1->2 2->3
                source: always equal to our 0 node
                sink: our target node
                alpha: adjustable value
                aslo_return_visited: whether we should also return the visited nodes

        VARIABLES:
                Influence: A priority queue(SortedDict): Node: influence
                Damage: Dictionary{}, key: Node, val: Priority Queue(SortedDict): Node: Damage

                ex. 1 -> 2 -> 3 
    """
    #print(graph.vcount()) #The number of vertices in the graph
    graph.vs['preColor'] = ['NA']*graph.vcount() #Adds a new attribute - pre-color to each NODE which tells us what the color of the edge from oldNode--Node is

    '''
    influence = SortedDict() #Initalize Influence- Priority Queue/Sorted Dict- Will hold Node: Influence
    influence = {}
    influence = SortedDict()
    influence.key=influence.get'''

    # create a chainmap containing two dictionaries: unvisited and visited nodes, respectively
    visited = {}
    influence = ChainMap(pqdict(), visited)

    Damage = defaultdict(dict) #Initalize Damage- Dictionary of: Priority Queue/Sorted Dic- Will hold: Node [Node] = Damge

    '''
    ## first, initialize values for every unvisited node
    for v in graph.vs: #Loops through all list vertices in the graph
        #print(v) #Prints the entire node object, ex: igraph.Vertex(<igraph.Graph object at 0x7fa1a70cfc70>, 0, {})
        #print(v.index) #Prints just the node itself, ex: 0
        #influence[v.index] = float('inf')
        influence[v.index] = float('inf')'''
    # influence = pqdict({v.index:float('inf') for v in graph.vs})## first, initialize values for every unvisited node

    # influence[source] = 0 #Set the source node to 0
    # node_influence = 0
    # influence.pop(source) #Pops of source

    #Damage[source] = SortedDict()
    Damage[source] = {}

    print("Influence Priority Queue:", influence)
    print()

    ##run a modified Dijkstra's algorithm
    #print("Source", source) #Currently source is just the number 0, or whatever node this corresponds to
    #print("Source Object", graph.vs.find(source)) #This finds the igraph object related to source
    source = graph.vs.find(source)
    visited[source] = 0

    vistedNodes=[] #The index(number only) of all nodes which have already been visited

    #Find all incoming edges of sink
    print("SINK")
    # sinkObjects = graph.vs.find(sink).in_edges()
    #sinkINT = set(sinkObject.source for sinkObject in sinkObjects)

    
    node = source #Node will hold our current node and starts with our source node-- This holds the igraph object
    #while node.index != sink: #while sink is unvisited
    while True:
        #sinkINT.discard(node.index)
        outEdges = node.out_edges() #Find all child nodes
        for i in outEdges: #Loop through all child nodes
            #print(i.target_vertex.index) #Just the node number
            #print(i.target_vertex) #The igraph object

            ##count the current edge
            #newInfluence = influence[node.index] + 1
            newInfluence = influence[node] + 1

            print("NODE", node.index)
            print("NewNode", i.target_vertex.index)

            ##check if the edge oldNode---node and node--new_node(i) are the same 'color'
            print("Attirbutes of Old Node--Node Edge, stored in Node", i.target_vertex.attributes())
            print("Attirbutes of Node--New Node Edge", i.attributes())
            #Old2Node = i.target_vertex.attributes()['preColor'] #This works as a dictionary, so we must pull the 'preColor' object out of it
            Old2Node = node['preColor']
            Node2New = i['type']
            print('OldNode--Node', Old2Node)
            print('Node--NewNode', Node2New)
            print()

            ### Can us te walkaround below instead-- if node != source: #If we have the source node, then we don't need to check the previous edge becuase it doesn't exist
            #First check to make sure that we are not at the source: NA, then if the edges still aren't equal then add alpha to influence
            if Old2Node != 'NA' and Old2Node != Node2New:
                newInfluence = newInfluence + alpha

            old_child_damage = Damage[i.target_vertex.index] #child
            new_child_damage = Damage[node.index] #node
            print("#####Influence Priority Queue:", influence)
            old_influence = influence.get(i.target_vertex, float('inf'))
            new_influence = newInfluence #The term we have been calculating above
            child = i.target_vertex.index #Child index
            child_damage = damage_at_child(old_child_damage, new_child_damage, old_influence, new_influence, child)
            Damage[child] = child_damage
            
            '''3/3/21 Moved this to damage_at_child function above
            for other in Damage[i.target_vertex.index].keys():
                print("Node", node.index)
                print("Child", i.target_vertex.index)
                print("Other", other)


                #if other not in Damage[node.index]:
                if other in Damage[node.index] and Damage[node.index][other] == float('inf'):
                    new_damge = float('inf')
                else:
                    new_damge = newInfluence - old_influence
                    print("------------------------------------------")
                    print("newInfluence", newInfluence)
                    print("Infludnce Child", old_influence)
                    print("New Damage", new_damge)
                ##Update Damage
                if other in Damage[i.target_vertex.index]:
                    current_damge = Damage[i.target_vertex.index][other]
                    final_damage = min(current_damge, new_damge)
                    Damage[i.target_vertex.index][other] = final_damage
                else:
                    Damage[i.target_vertex.index][other] = new_damge

            if old_influence > newInfluence: #If we are on the best path
                Damage[i.target_vertex.index][i.target_vertex.index] = float('inf')
                Damage[i.target_vertex.index].update(Damage[node.index]) #Copies all values from node.index into child.inex
            #Ensures that the sorted dictionarires will contain the nodes of the best path from source(not included) to node            
            '''


            ##Update inflence function
            if old_influence > newInfluence: #If we want to take this path?
               influence[i.target_vertex] = newInfluence
               print("WE are updating ", i.target_vertex.index , "to ", str(Node2New))
               i.target_vertex['preColor'] = str(Node2New)


            print("Influence Priority Queue:", influence)
            print("Damges", Damage)


        try:
            node, node_influence = influence.popitem() #This will pop off (and remove) the min unvisited influence
        except KeyError:
            # if there are no longer any more nodes to visit, just exit the loop
            break
        visited[node] = node_influence # add the node and its influence to the dict of visited nodes
        """
        nodeID, node_influence = influence.popitem() #This will pop off (and remove) the min item in our list
        node = graph.vs.find(nodeID)
        """


        '''
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
                break'''
        
    
    #del Damage[sink][sink]
    Damage[sink].pop(sink, None)

    ##Check Point
    print("----------------------------------------------------------------------------")
    print("Final Node: ", node.index)
    print("Influence Priority Queue:", influence)
    print("Damage:", Damage)
    print("Damage SINK:", Damage[sink])
    #print("PEEK", max(Damage[sink], key = Damage[sink].get))

    if also_return_visited:
        return Damage[sink], visited
    return Damage[sink]

def most_detrimental(graph, source, sink, alpha=1, also_return_visited=False):
    """
        return a node that, when removed, will cause the most damage to a shortest path
        between source and sink in the directed graph
    """
    print("Graph Edges", graph.get_edgelist())
    print("Graph Type", graph.es['type'])
    
    #print(graph.es.attributes())
    #print(graph.vs.find(14))
    #return()
    print("Check index", graph.vs.find(source))
    source = graph.vs.find(source).index
    sink = graph.vs.find(sink).index
    #print(source, sink)
    print()

    if also_return_visited:
        damages, visited = damage(graph, source, sink, alpha, also_return_visited)
    else:
        damages = damage(graph, source, sink, alpha)
    #Damges = priority queue (SortedDict object): only has the sink node ('one-column'), 
    #{sink:{"node1": "damage of removing node1 in path from source to sink", "node2: "....""}}

    maxIndex = None
    try:
        maxIndex = max(damages, key = damages.get) #Finding the maximum node from the priority queue  Damages
        #print(graph.vs[maxIndex]["name"])
        if "name" in graph.vs[maxIndex].attributes():
            maxIndex = graph.vs[maxIndex]["name"]
    except ValueError:
        pass #Doesn't do anything
    
    if also_return_visited:
        return maxIndex, visited
    return maxIndex

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
@click.option("--plot", help="also write a plot of the visited nodes to the provided file")
def read_sif(fname, source, sink, alpha=1, plot=None):
    """ Run the most detrimental node finder on an SIF file """

    # first import pandas and load the sif adjacency list into a dataframe
    import pandas as pd
    df = pd.read_csv(fname, sep = "\t", names = ["to","edge","from"], dtype=str)
    color_map = dict(zip(sorted(df['edge'].unique()), ('blue', 'red')))

    # convert to a graph
    graph = igraph.Graph.TupleList(df[["to","from"]].itertuples(index=False), directed = True)
    graph.es['type'] = df["edge"]

    # what does igraph think is the best path?
    # print(graph.get_shortest_paths(graph.vs.find(source), graph.vs.find(sink)))

    # run the most detrimenal node finder
    if plot:
        node, visited = most_detrimental(graph, source, sink, alpha, True)

        # subset the graph to just the nodes that were visited
        graph = graph.induced_subgraph(visited.keys())
        # add node labels, node colors, and edge colors
        graph.vs["label"] = graph.vs["name"]
        graph.vs.find(source)["color"] = 'green'
        graph.vs.find(sink)["color"] = 'green'
        graph.vs.find(node)["color"] = 'yellow'
        graph.es["color"] = [color_map[edge_type] for edge_type in graph.es['type']]
        # make the plots pretty
        visual_style = {}
        visual_style["vertex_size"] = 50
        visual_style["vertex_label_size"] = 25
        visual_style["edge_width"] = 4

        # write a plot of the nodes that were visited
        igraph.plot(graph, plot, **visual_style)
    else:
        node = most_detrimental(graph, source, sink, alpha)

    # output the most detrimental node
    click.echo('{}'.format(node))


if __name__ == "__main__":
    print(main(sys.argv[1]))
