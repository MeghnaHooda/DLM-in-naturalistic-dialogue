#SEGREGATING SENTENCE STRUCTURE WITH DIFFERENT WORD ORDER : SOV/OSV for dialogue corpus

import os
import csv
import sys
from io import open
from conllu import parse
import networkx as nx
from networkx.algorithms.traversal.depth_first_search import dfs_tree

sys.path.append("C:/Users/meghn/OneDrive/Documents/Psycholing/DLM_Data_Analysis/Measures") #Put the path of Measures folder here

from Measures import num_cross, dependency_distance, dependency_direction

def find_subj_obj(directory, Sentence, file_out1, file_out2):
    ud_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.conllu'):
                fullpath = os.path.join(root, file)
                ud_files.append(fullpath)            # creates a list of path of all files (file of each language) from the directory
    print("total files found:",len(ud_files))
    # creating csv files
    mycsvfile1 = open(file_out1, 'w+', encoding='utf-8')
    mycsvfile2 = open(file_out2, 'w+', encoding='utf-8')

    csvwriter1 = csv.writer(mycsvfile1) 
    csvwriter1.writerow(['File','Sent_ID','Sentence','Length','Word Order','Category', 'dependency length'])
    csvwriter2 = csv.writer(mycsvfile2)
    csvwriter2.writerow(['File','Sent_ID','Sentence','Length','Word Order','Category', 'dependency length',
                        'sub ID','subject','sub_subset_words','sub_subset_length','sub_subset_char_length','sub_difluency','sub_hesitation','sub_repair',
                        'obj ID','object','obj_subset_words','obj_subset length','obj_subset_char_length','obj_difluency','obj_hesitation','obj_repair',
                        'iobj ID','iobject','iobj_subset_words','iobj_subset_length','iobj_subset_char_length',
                        ])

    tags=['pause','laughter','noise','aside','b_aside','e_aside'] #list of tags that needed to be removed from subtree
    misc_tags=['Repair','Hesitation','Disfluency']  #List of tags in misc that needed to be removed from subtree
    print(ud_files)
    if len(ud_files)>0:
        for i in ud_files:                                       # reads file of each language one by one
            count=0
            lang = str(i)
            # print(lang)
            data_file = open(str(i),'r',encoding='utf-8').read()
            sentences = []
            sentences = parse(data_file)
            sent_id=0

            for sentence in sentences[0:]:
                sent_id+=1
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
                nsubj=[]
                obj=[]
                iobj=[]
                verb_index=[]
                for nodex in tree.nodes:
                    if not nodex==0:
                        if tree.nodes[nodex]['upostag']=='VERB':
                            # if tree.nodes[nodex]['head']==0:
                            # verb_index.append(nodex)
                            verb_temp=nodex
                            nsubj_temp=0
                            obj_temp=0
                            iobj_temp=0
                            for nodex in tree.nodes:
                                if not nodex==0:
                                    if tree.nodes[nodex]['deprel']=='nsubj' and tree.nodes[nodex]['head']==verb_temp:
                                        nsubj_temp=nodex
                                    if tree.nodes[nodex]['deprel']=='obj' and tree.nodes[nodex]['head']==verb_temp:
                                        obj_temp=nodex
                                    if tree.nodes[nodex]['deprel']=='iobj' and tree.nodes[nodex]['head']==verb_temp:
                                        iobj_temp=nodex
                            if nsubj_temp!=0 and obj_temp!=0:
                                verb_index.append(verb_temp)
                                nsubj.append(nsubj_temp)
                                obj.append(obj_temp)
                                if iobj_temp!=0:
                                    iobj.append(iobj_temp)
                                else:
                                    iobj.append(0)
                dd=[]
                for edgex in tree.edges:
                    if not edgex[0]==ROOT:
                        dd_temp=dependency_distance(tree, ROOT,edgex)
                        dd.append(dd_temp)
                
                for v_i_i in range(0,len(verb_index)):
                    # print(nsubj[v_i_i],obj[v_i_i], iobj[v_i_i])
                    category=0
                    if nsubj[v_i_i]!=0 and obj[v_i_i]!=0 and iobj[v_i_i]==0:
                        category="Transitive"
                    elif nsubj[v_i_i]!=0 and obj[v_i_i]!=0 and iobj[v_i_i]!=0:
                        # print("ditransitive sentence",sentence)
                        category="Ditransitive"
                    
                    obj_words=[]
                    nsubj_words=[]
                    iobj_words=[]

                    cross=False

                    nsubj_subtree = dfs_tree(tree, nsubj[v_i_i])
                    case_marker_head=0
                    nsubj_difluency=0
                    nsubj_hesitation=0
                    nsubj_repair=0
                    for nodex_subtree in nsubj_subtree:
                        if not nodex_subtree==0:
                            if tree.nodes[nodex_subtree]['misc'] is not None:
                                misc_column=list(tree.nodes[nodex_subtree]['misc'].keys())[0]
                            else:
                                misc_column=None
                            if tree.nodes[nodex_subtree]['form'] not in tags and misc_column not in misc_tags:
                                nsubj_words.append(tree.nodes[nodex_subtree]['form'])
                            elif misc_column == 'Disfluency':
                                nsubj_difluency=1
                            elif misc_column == 'Hesitation':
                                nsubj_hesitation=1
                            elif misc_column == 'Repair':
                                nsubj_repair=1
                            if tree.nodes[nodex_subtree]['deprel']=='case':
                                case_marker=nodex_subtree
                                case_marker_head=tree.nodes[nodex_subtree]['head']
                                case_marker_object=str(tree.nodes[case_marker_head]['form'])+" "+str(tree.nodes[nodex_subtree]['form'])
                                nsubj_words.append(case_marker_object)
                            if case_marker_head!=0:
                                if tree.nodes[case_marker_head]['form'] in nsubj_words:
                                    nsubj_words.remove(tree.nodes[case_marker_head]['form'])
                                if tree.nodes[case_marker]['form'] in nsubj_words:
                                    nsubj_words.remove(tree.nodes[case_marker]['form'])
                            if tree.nodes[nodex_subtree]['head']> verb_index[v_i_i]:
                                cross=True
                    obj_subtree = dfs_tree(tree,obj[v_i_i])
                    case_marker_head=0
                    obj_difluency=0
                    obj_hesitation=0
                    obj_repair=0
                    for nodex_subtree in obj_subtree:
                        if not nodex_subtree==0:
                            if tree.nodes[nodex_subtree]['misc'] is not None:
                                misc_column=list(tree.nodes[nodex_subtree]['misc'].keys())[0]
                            else:
                                misc_column=None
                            if tree.nodes[nodex_subtree]['form'] not in tags and misc_column not in misc_tags :
                                obj_words.append(tree.nodes[nodex_subtree]['form'])
                            elif misc_column == 'Disfluency':
                                obj_difluency=1
                            elif misc_column == 'Hesitation':
                                obj_hesitation=1
                            elif misc_column == 'Repair':
                                obj_repair=1
                            if tree.nodes[nodex_subtree]['deprel']=='case':
                                case_marker=nodex_subtree
                                case_marker_head=tree.nodes[nodex_subtree]['head']
                                case_marker_object=str(tree.nodes[case_marker_head]['form'])+" "+str(tree.nodes[nodex_subtree]['form'])
                                obj_words.append(case_marker_object)
                            if case_marker_head!=0:
                                if tree.nodes[case_marker_head]['form'] in obj_words:
                                    obj_words.remove(tree.nodes[case_marker_head]['form'])
                                if tree.nodes[case_marker]['form'] in obj_words:
                                    obj_words.remove(tree.nodes[case_marker]['form'])
                            if tree.nodes[nodex_subtree]['head']> verb_index[v_i_i]:
                                cross=True
                    if iobj[v_i_i]!=0:
                        if iobj[v_i_i]>verb_index[v_i_i]:
                            cross=True
                        iobj_subtree = dfs_tree(tree, nsubj[v_i_i])
                        case_marker_head=0
                        for nodex_subtree in iobj_subtree:
                            if not nodex_subtree==0:
                                if tree.nodes[nodex_subtree]['misc'] is not None:
                                    misc_column=list(tree.nodes[nodex_subtree]['misc'].keys())[0]
                                else:
                                    misc_column=None
                                if tree.nodes[nodex_subtree]['form'] not in tags and misc_column not in misc_tags :
                                    iobj_words.append(tree.nodes[nodex_subtree]['form'])
                                if tree.nodes[nodex_subtree]['deprel']=='case':
                                    case_marker=nodex_subtree
                                    case_marker_head=tree.nodes[nodex_subtree]['head']
                                    case_marker_object=str(tree.nodes[case_marker_head]['form'])+" "+str(tree.nodes[nodex_subtree]['form'])
                                    # print(obj_words, tree.nodes[case_marker_head]['form'])
                                    iobj_words.append(case_marker_object)
                                if case_marker_head!=0:
                                    if tree.nodes[case_marker_head]['form'] in iobj_words:
                                        iobj_words.remove(tree.nodes[case_marker_head]['form'])
                                    if tree.nodes[case_marker]['form'] in iobj_words:
                                        iobj_words.remove(tree.nodes[case_marker]['form'])
                                if tree.nodes[nodex_subtree]['head']> verb_index[v_i_i]:
                                        cross=True
                    word_order=""
                    if category!=0: #and cross==False:
                        if num_cross(tree, obj[v_i_i], verb_index[v_i_i]) ==0 and num_cross(tree, nsubj[v_i_i], verb_index[v_i_i])==0:
                            if nsubj[v_i_i]<verb_index[v_i_i] and obj[v_i_i]<verb_index[v_i_i]:
                                if nsubj[v_i_i]<obj[v_i_i]<verb_index[v_i_i]:
                                    word_order="SOV"
                                    if iobj[v_i_i]!=0:
                                        if iobj[v_i_i]>nsubj[v_i_i] and iobj[v_i_i]<obj[v_i_i]:
                                            word_order="S-IO-O-V"
                                        elif iobj[v_i_i]<nsubj[v_i_i] and iobj[v_i_i]<obj[v_i_i]:
                                            word_order="IO-S-O-V"
                                        elif iobj[v_i_i]>nsubj[v_i_i] and iobj[v_i_i]>obj[v_i_i]:
                                            word_order="S-O-IO-V"
                                elif obj[v_i_i]<nsubj[v_i_i]<verb_index[v_i_i]:
                                    word_order="OSV"
                                    if iobj[v_i_i]!=0:
                                        if iobj[v_i_i]>obj[v_i_i] and iobj[v_i_i]<nsubj[v_i_i]:
                                            word_order="O-IO-S-V"
                                        elif iobj[v_i_i]<obj[v_i_i] and iobj[v_i_i]<nsubj[v_i_i]:
                                            word_order="IO-O-S-V"
                                        elif iobj[v_i_i]>obj[v_i_i] and iobj[v_i_i]>nsubj[v_i_i]:
                                            word_order="O-S-IO-V"
                                else:
                                    word_order="Others"
                                # elif obj[v_i_i]<verb_index[v_i_i]<nsubj[v_i_i]:
                                #     word_order="OVS"
                                # elif nsubj[v_i_i]<verb_index[v_i_i]<obj[v_i_i]:
                                #     word_order="SVO"
                                # elif verb_index[v_i_i]<nsubj[v_i_i]<obj[v_i_i]:
                                #     word_order="VSO"
                                # elif verb_index[v_i_i]<obj[v_i_i]<nsubj[v_i_i]:
                                #     word_order="VOS"
                            
                                row1=[
                                lang,
                                sent_id,
                                sentence.metadata[Sentence],
                                n+1,
                                word_order,
                                category,
                                sum(dd)/len(dd)
                                ]
                                csvwriter1.writerow(row1) #saving 
                                
                                #Character length for nsubj, obj and iobj
                                nsubj_char_len=0
                                for nsubj_word in nsubj_words:
                                    char_len = len(nsubj_word.replace(" ",""))
                                    nsubj_char_len+=char_len
                                obj_char_len=0
                                for obj_word in obj_words:
                                    char_len = len(obj_word.replace(" ",""))
                                    obj_char_len+=char_len


                                if iobj[v_i_i]!=0:
                                    iobj_char_len=0
                                    for iobj_word in iobj_words:
                                        char_len= len(iobj_word.replace(" ",""))
                                        iobj_char_len+=char_len
                                    csvwriter2.writerow([lang,
                                                        sent_id,
                                                        sentence.metadata[Sentence],
                                                        n+1,
                                                        word_order,
                                                        category,
                                                        sum(dd)/len(dd),
                                                        nsubj[v_i_i],
                                                        tree.nodes[nsubj[v_i_i]]['form'],
                                                        nsubj_words,
                                                        len(nsubj_words),
                                                        nsubj_char_len,
                                                        nsubj_difluency,
                                                        nsubj_hesitation,
                                                        nsubj_repair,
                                                        obj[v_i_i],
                                                        tree.nodes[obj[v_i_i]]['form'],
                                                        obj_words,
                                                        len(obj_words),
                                                        obj_char_len,
                                                        obj_difluency,
                                                        obj_hesitation,
                                                        obj_repair,
                                                        iobj[v_i_i],
                                                        tree.nodes[iobj[v_i_i]]['form'],
                                                        iobj_words,
                                                        len(iobj_subtree),
                                                        iobj_char_len
                                                        ])
                                else:
                                    csvwriter2.writerow([lang,
                                                        sent_id,
                                                        sentence.metadata[Sentence],
                                                        n+1,
                                                        word_order,
                                                        category,
                                                        sum(dd)/len(dd),
                                                        nsubj[v_i_i],
                                                        tree.nodes[nsubj[v_i_i]]['form'],
                                                        nsubj_words,
                                                        len(nsubj_words),
                                                        nsubj_char_len,
                                                        nsubj_difluency,
                                                        nsubj_hesitation,
                                                        nsubj_repair,
                                                        obj[v_i_i],
                                                        tree.nodes[obj[v_i_i]]['form'],
                                                        obj_words,
                                                        len(obj_words),
                                                        obj_char_len,
                                                        obj_difluency,
                                                        obj_hesitation,
                                                        obj_repair,
                                                        ])

# directory_dia = "../Dialouge Corpus Filttered/parse_gold_filttered"                    # directory containing the Dialogue corpus tree files in CONLLU format
# find_subj_obj(directory_dia, 'Sentence', 'nsubj_obj.csv','token_wise_nsubj_obj.csv')

directory_txt="../UD_Hindi-HDTB" #Change this to the dialouge data for dialogue data analysis
find_subj_obj(directory_txt, 'text','nsubj_obj_txt.csv','token_wise_nsubj_obj_txt.csv')