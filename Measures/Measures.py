#PROJECTIVITY MODULE

import os
import csv
from io import open
from conllu import parse
import networkx as nx
from networkx.algorithms.traversal.depth_first_search import dfs_tree

def num_cross(tree,abs_root,ROOT):               # requires tree, abs=head, ROOT=dependent
    ncross=0
    for edgex in tree.edges:
        if not edgex[0]==abs_root:
            if is_projective(tree, edgex, ROOT):                   # checks if edge is projective or not
                ncross+= 0
            else:
                ncross += 1
    return ncross


def is_projective(tree, edge, root):             # Checks if an edge is projective or not and returns a boolean value.
    projective=True
    edge_span=[]                 
    if edge[0]>edge[1]:                                      
        for nodex in nx.descendants(tree, root):   
            if edge[1]<nodex<edge[0]:
                edge_span.append(nodex)                       
    else:
        for nodex in nx.descendants(tree, root):
            if edge[0]<nodex<edge[1]:
                edge_span.append(nodex)
    flag=0
    for nodeI in edge_span:
        if not tree.nodes[nodeI]['head'] in edge_span:
            if not nodeI in nx.descendants(tree, edge[0]):
                if not tree.nodes[nodeI]['deprel']=='punct':
                    flag += 1
    if not flag==0:
        projective=False
    return projective


def dependency_distance(tree, root, edge):        # Computes the dependency length i.e., no. of nodes between head and its dependent 
    dd=0
    if edge[0]>edge[1]:                      
        for nodex in nx.descendants(tree, root):        
            if edge[1]<=nodex<edge[0]:                             # all the nodes that lies linearly between dependent and head   
                dd+=1
    else:
        for nodex in nx.descendants(tree, root):
            if edge[0]<=nodex<edge[1]:
                dd+=1
    return dd

def dependency_direction(edge):       # Computes the direction of an edge (i.e., dependency) according to relative position of dependent and head  
    direction=''
    if edge[0]>edge[1]:                     # edge is a list data type in the format [head,dependent]
        direction='RL'
    else:
        direction='LR'

    return direction  

