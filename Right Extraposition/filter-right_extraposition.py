#SEGREGATING SENTENCE STRUCTURE WITH DIFFERENT non projective sentences for dialogue corpus
# the filtering criteria is:
#Filter the word in the sentence that generate crossing (the Noun)-- dpen_id, obtain its head(Verb)--head1 and its child--head2.
#If depen_id<head1<head2 --> then non projective right extrapose

import os
import csv
import sys
from io import open
from conllu import parse
import networkx as nx
from networkx.algorithms.traversal.depth_first_search import dfs_tree

sys.path.append("C:/Users/meghn/OneDrive/Documents/Psycholing/DLM_ICM_Data_Analysis/Word Order Analysis 2/Measures")

from Measures import num_cross, dependency_distance, dependency_direction


def fin_non_projective_instances(directory, Sentence, file_out1):
    ud_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.conllu'):
                fullpath = os.path.join(root, file)
                ud_files.append(fullpath)            # creates a list of path of all files (file of each language) from the directory
    print("total files found:",len(ud_files))
    # creating csv files
    mycsvfile1 = open(file_out1, 'w+', encoding='utf-8')
    # mycsvfile2 = open(file_out2, 'w+', encoding='utf-8')

    csvwriter1 = csv.writer(mycsvfile1) 
    csvwriter1.writerow(['File','Sent_ID','Sentence','Length', 'Category', 'dep_Length' ,'Dependency Length'])

    # csvwriter2 = csv.writer(mycsvfile2)
    # csvwriter2.writerow(['File','Sent_ID','Sentence','Length','Category', 'dep_Length','Dependency Length'])
    if len(ud_files)>0:
        for i in ud_files:                                       # reads file of each language one by one
            lang = str(i)
            # print(lang)
            data_file = open(str(i),'r',encoding='utf-8').read()
            sentences = []
            sentences = parse(data_file)
            # sent_id=0

            for sentence in sentences[0:]:
                # sent_id+=1
                tree = nx.DiGraph()                              # An empty directed graph (i.e., edges are uni-directional)
                for nodeinfo in sentence[0:]:                    # retrieves information of each node from dependency tree in UD format
                    entry=list(nodeinfo.items())
                    if not entry[7][1]=='punct':
                        tree.add_node(entry[0][1], form=entry[1][1], lemma=entry[2][1], upostag=entry[3][1], xpostag=entry[4][1], feats=entry[5][1], head=entry[6][1], deprel=entry[7][1], deps=entry[8][1], misc=entry[9][1])                #adds node to the directed graph
                ROOT=0
                tree.add_node(ROOT)                            # adds an abstract root node to the directed graph

                for nodex in tree.nodes:
                    if not nodex==0:
                        if tree.has_node(tree.nodes[nodex]['head']):                                         # to handle disjoint trees
                            tree.add_edge(tree.nodes[nodex]['head'],nodex,drel=tree.nodes[nodex]['deprel'])       # adds edges as relation between nodes

                n=len(tree.edges) #length of sentence without punctuation
                # num_crossing = num_cross(tree,1000,ROOT)
                num_of_cross=0

                for nodex in tree.nodes:
                    if not nodex==0:
                        if num_cross(tree, nodex, ROOT)!=0:
                            num_of_cross+=1
                
                depen_id=0
                head1=0
                head2=0
                if num_of_cross==0:
                    for nodex in tree.nodes:
                        if not nodex==0:
                            if tree.nodes[nodex]['deprel']=='nmod':
                                depen_id=nodex
                                head1 = tree.nodes[nodex]['head']
                                if head1!=0:
                                    head2 = tree.nodes[head1]['head']
                                    depen_id_subtree_count=0
                                    if depen_id<head1<head2:
                                        depen_id_subtree=dfs_tree(tree,depen_id)
                                        for i in depen_id_subtree.nodes:
                                            if i != head1:
                                                depen_id_subtree_count+=1
                                        dd=[]
                                        for edgex in tree.edges:
                                            if not edgex[0]==ROOT:
                                                dd_temp=dependency_distance(tree, ROOT,edgex)
                                                dd.append(dd_temp)
                                        row1=[
                                            lang,
                                            sentence.metadata['sent_id'],
                                            sentence.metadata[Sentence],
                                            n+1,
                                            'nmod',
                                            depen_id_subtree_count,
                                            sum(dd)/len(dd)
                                            ]
                                        csvwriter1.writerow(row1) #saving 
                            elif tree.nodes[nodex]['deprel']=='acl:relcl':
                                depen_id=nodex
                                head1 = tree.nodes[nodex]['head']
                                if head1!=0:
                                    head2 = tree.nodes[head1]['head']
                                    depen_id_subtree_count=0
                                    if head1<depen_id<head2:
                                        depen_id_subtree=dfs_tree(tree,depen_id)
                                        for i in depen_id_subtree.nodes:
                                            if i != head1:
                                                depen_id_subtree_count+=1
                                        dd=[]
                                        for edgex in tree.edges:
                                            if not edgex[0]==ROOT:
                                                dd_temp=dependency_distance(tree, ROOT,edgex)
                                                dd.append(dd_temp)
                                        csvwriter1.writerow([lang,
                                                             sentence.metadata['sent_id'],
                                                             sentence.metadata[Sentence],
                                                             n+1,
                                                             'acl:relcl',
                                                             depen_id_subtree_count,
                                                             sum(dd)/len(dd)
                                                             ])

# directory_dia = "../Dialouge Corpus Filttered/parse_gold_filttered"                    # directory containing the Dialogue corpus tree files in CONLLU format
# directory_dia_test = "./"
# fin_non_projective_instances(directory_dia, 'Sentence','nmod_relcl_sentences.csv') #For Dialogue Data

directory_txt = "../UD_Hindi-HDTB/Phase1"
fin_non_projective_instances(directory_txt, 'text','nmod_relcl_sentences_txt.csv')
