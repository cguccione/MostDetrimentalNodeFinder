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
        child_damage = new_child_damage.copy()
        for node, damage in new_child_damage.items(): #new_child_damage -- shoudln't contain itself (the child)
            if node in old_child_damage: #Will be true if we have alread touched this child ## True for node 1 but not node 4
                updated_damage = old_child_damage[node] + new_damage
            else:
                updated_damage = new_damage
            child_damage[node] = min(damage, updated_damage)

    else: #Updating the old damages
        new_damage = new_influence - old_influence
        child_damage = old_child_damage
        for node, damage in old_child_damage.items():
            if node in new_child_damage: #Already have a damage- 
                updated_damage = new_child_damage[node] + new_damage
            else:
                updated_damage = new_damage
            child_damage[node] = min(damage, updated_damage)

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
    graph.vs['preColor'] = ['NA']*graph.vcount() #Adds a new attribute - pre-color to each NODE which tells us what the color of the edge from oldNode--Node is

    # create a chainmap containing two dictionaries: unvisited and visited nodes, respectively
    visited = {}
    influence = ChainMap(pqdict(), visited)

    Damage = defaultdict(dict) #Initalize Damage- Dictionary of: Priority Queue/Sorted Dic- Will hold: Node [Node] = Damge

    Damage[source] = {}

    ##run a modified Dijkstra's algorithm
    source = graph.vs.find(source)
    visited[source] = 0

    vistedNodes=[] #The index(number only) of all nodes which have already been visited

    sinkObjects = graph.vs.find(sink).in_edges()
    sinkINT = set(sinkObject.source for sinkObject in sinkObjects)
    
    node = source #Node will hold our current node and starts with our source node-- This holds the igraph object
    while len(sinkINT):
        sinkINT.discard(node.index)
        outEdges = node.out_edges() #Find all child nodes
        for i in outEdges: #Loop through all child nodes
       
            newInfluence = influence[node] + 1

            #Old2Node = i.target_vertex.attributes()['preColor'] #This works as a dictionary, so we must pull the 'preColor' object out of it
            Old2Node = node['preColor']
            Node2New = i['type']

            ### Can us te walkaround below instead-- if node != source: #If we have the source node, then we don't need to check the previous edge becuase it doesn't exist
            #First check to make sure that we are not at the source: NA, then if the edges still aren't equal then add alpha to influence
            if Old2Node != 'NA' and Old2Node != Node2New:
                newInfluence = newInfluence + alpha

            old_child_damage = Damage[i.target_vertex.index] #child
            new_child_damage = Damage[node.index] #node
            old_influence = influence.get(i.target_vertex, float('inf'))
            new_influence = newInfluence #The term we have been calculating above
            child = i.target_vertex.index #Child index
            child_damage = damage_at_child(old_child_damage, new_child_damage, old_influence, new_influence, child)
            Damage[child] = child_damage

            ##Update inflence function
            if old_influence > newInfluence: #If we want to take this path?
               influence[i.target_vertex] = newInfluence
               i.target_vertex['preColor'] = str(Node2New)

        try:
            node, node_influence = influence.popitem() #This will pop off (and remove) the min unvisited influence
        except KeyError:
            # if there are no longer any more nodes to visit, just exit the loop
            break
        visited[node] = node_influence # add the node and its influence to the dict of visited nodes    
    
    Damage[sink].pop(sink, None) #Remove the sink, sink node

    if also_return_visited:
        return Damage[sink], visited
    return Damage[sink]

def most_detrimental(graph, source, sink, alpha=1, also_return_visited=False):
    """
        return a node that, when removed, will cause the most damage to a shortest path
        between source and sink in the directed graph
    """
    source = graph.vs.find(source).index
    sink = graph.vs.find(sink).index

    if also_return_visited:
        damages, visited = damage(graph, source, sink, alpha, also_return_visited)
    else:
        damages = damage(graph, source, sink, alpha)
        #Damges = priority queue (SortedDict object): only has the sink node ('one-column'), 
        #{sink:{"node1": "damage of removing node1 in path from source to sink", "node2: "....""}}

    maxIndex = None
    try:
        maxIndex = max(damages, key = damages.get) #Finding the maximum node from the priority queue  Damages
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
    color_map = dict(zip(sorted(df['edge'].unique()), ('#7adefa', '#f06c67')))

    # convert to a graph
    graph = igraph.Graph.TupleList(df[["to","from"]].itertuples(index=False), directed = True)
    graph.es['type'] = df["edge"]

    # run the most detrimenal node finder
    if plot:
        node, visited = most_detrimental(graph, source, sink, alpha, True)
        newgraph = graph.get_all_simple_paths(source, to =sink)

        nodes = set(n for path in newgraph for n in path)
        graph = graph.induced_subgraph(nodes)


        # add node labels, node colors, and edge colors
        graph.vs["label"] = graph.vs["name"]
        for n in graph.vs:
            n["color"] = '#171716'
        graph.vs.find(source)["color"] = 'red'
        graph.vs.find(sink)["color"] = 'blue'
        graph.vs.find(node)["color"] = '#ab0595'
        graph.es["color"] = [color_map[edge_type] for edge_type in graph.es['type']]
        # make the plots pretty
        visual_style = {}
        visual_style["vertex_size"] = 50
        visual_style["vertex_label_size"] = 2
        visual_style["edge_width"] = 8
        visual_style["bbox"] = (3000, 3000)
        visual_style["edge_arrow_size"] = 6
        visual_style["layout"] = graph.layout('kk')


        # write a plot of the nodes that were visited
        igraph.plot(graph, plot, **visual_style)
    else:
        node = most_detrimental(graph, source, sink, alpha)

    # output the most detrimental node
    click.echo('{}'.format(node))


if __name__ == "__main__":
    print(main(sys.argv[1]))
