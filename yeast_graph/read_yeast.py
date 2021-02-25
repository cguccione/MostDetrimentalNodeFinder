#!/usr/bin/env python
import pytest
import pandas as pd
from igraph import Graph

file = "data/yeast_GPN.sif"
yeast_df = pd.read_csv(file, sep = "\t", names = ["to","edge","from"])
yeast_graph = Graph.DataFrame(yeast_df[["to","from"]], directed = True)
yeast_graph.es['type'] = yeast_df["edge"]

