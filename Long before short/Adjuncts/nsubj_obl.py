#SEGREGATING SENTENCE STRUCTURE WITH DIFFERENT WORD ORDER like SOblV/OblSV for dialogue corpus

import os
import csv
import sys
from io import open
from conllu import parse
import networkx as nx
from networkx.algorithms.traversal.depth_first_search import dfs_tree

sys.path.append("C:/Users/meghn/OneDrive/Documents/Psycholing/DLM_Data_Analysis/Measures") #Put the path of Measures folder here

from Measures import num_cross, dependency_distance, dependency_direction


def fin_nsubj_obl(directory, Sentence, file_out1, file_out2):
    count=0
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
    csvwriter1.writerow(['File','Sent_ID','Sentence','Length','Category', 'Average Dependency'])
    csvwriter2 = csv.writer(mycsvfile2)
    csvwriter2.writerow(['File','Sent_ID','Sentence','Length','Category','Average Dependency',
                        'sub ID','subject','sub_subset_words','sub_subset_length','sub_subset_char_length','sub_direction',
                        'obl ID','obl','obl_subset_words','obl_subset_length','obl_subset_char_length','obl_direction',
                        ])

    tags=['pause','laughter','noise','aside','b_aside','e_aside'] #list of tags that needed to be removed from subtree
    misc_tags=['Repair','Hesitation','Disfluency']  #List of tags in misc that needed to be removed from subtree

    if len(ud_files)>0:
        for i in ud_files:                                       # reads file of each language one by one
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
                obl=[]
                verb_index=[]
                for nodex in tree.nodes:
                    if not nodex==0:
                        if tree.nodes[nodex]['upostag']=='VERB':
                            verb_temp=nodex
                            nsubj_temp=0
                            obl_temp=[]
                            obj_temp=0
                            for nodex in tree.nodes:
                                if not nodex==0:
                                    if tree.nodes[nodex]['deprel']=='nsubj' and tree.nodes[nodex]['head']==verb_temp:
                                        nsubj_temp=nodex
                                    if tree.nodes[nodex]['deprel']=='obl' and tree.nodes[nodex]['head']==verb_temp:
                                        obl_temp.append(nodex)
                                    if tree.nodes[nodex]['deprel']=='obj' and tree.nodes[nodex]['head']==verb_temp:
                                        obj_temp=nodex
                            if nsubj_temp!=0 and len(obl_temp)==1 and obj_temp==0:
                                verb_index.append(verb_temp)
                                nsubj.append(nsubj_temp)
                                obl.append(obl_temp[0])

                # if len(verb_index)>0:
                #     print(lang, sent_id, nsubj, obl, verb_index)
                #     count+=1
                dd=[]
                for edgex in tree.edges:
                    if not edgex[0]==ROOT:
                        dd_temp=dependency_distance(tree, ROOT,edgex)
                        dd.append(dd_temp)

                for v_i_i in range(0,len(verb_index)):
                    # print(num_cross(tree,nsubj[v_i_i],verb_index[v_i_i]))
                    # print(num_cross(tree,obl[v_i_i],ROOT))
                    # print(num_cross(tree,verb_index[v_i_i],ROOT))
                    
                    nsubj_words=[]
                    obl_words=[]

                    nsubj_subtree = dfs_tree(tree, nsubj[v_i_i])
                    case_marker_head=0
                    for nodex_subtree in nsubj_subtree:
                        if not nodex_subtree==0:
                            if tree.nodes[nodex_subtree]['misc'] is not None:
                                misc_column=list(tree.nodes[nodex_subtree]['misc'].keys())[0]
                            else:
                                misc_column=None
                            if tree.nodes[nodex_subtree]['form'] not in tags and misc_column not in misc_tags:
                                nsubj_words.append(tree.nodes[nodex_subtree]['form'])
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
                    
                    nsubj_subtree_dir=[] #direction fo the subtree from nsubj
                    for edgex in nsubj_subtree.edges:
                        if tree.nodes[edgex[1]]['misc'] is not None:
                            misc_column=list(tree.nodes[edgex[1]]['misc'].keys())[0]
                        else:
                            misc_column=None
                        if edgex[0]==nsubj[v_i_i] and misc_column not in misc_tags:
                            nsubj_subtree_dir.append(dependency_direction(edgex))
                    
                    nsubj_direction = 0
                    if len(nsubj_subtree_dir)==0:
                        nsubj_direction="No Direction"
                    else:
                        RL=0
                        LR=0
                        for value in nsubj_subtree_dir:
                            if value =='RL':
                                RL+=1
                            elif value =='LR':
                                LR+=1
                        if RL==LR==0:
                            nsubj_direction='No Direction'
                        elif RL==LR:
                            nsubj_direction='Both'
                        elif RL>LR:
                            nsubj_direction='RL'
                        elif LR>RL:
                            nsubj_direction='LR'
                        

                    obl_subtree = dfs_tree(tree,obl[v_i_i])
                    case_marker_head=0
                    for nodex_subtree in obl_subtree:
                        if not nodex_subtree==0:
                            if tree.nodes[nodex_subtree]['misc'] is not None:
                                misc_column=list(tree.nodes[nodex_subtree]['misc'].keys())[0]
                            else:
                                misc_column=None
                            if tree.nodes[nodex_subtree]['form'] not in tags and misc_column not in misc_tags :
                                obl_words.append(tree.nodes[nodex_subtree]['form'])
                            if tree.nodes[nodex_subtree]['deprel']=='case':
                                case_marker=nodex_subtree
                                case_marker_head=tree.nodes[nodex_subtree]['head']
                                case_marker_object=str(tree.nodes[case_marker_head]['form'])+" "+str(tree.nodes[nodex_subtree]['form'])
                                obl_words.append(case_marker_object)
                            if case_marker_head!=0:
                                if tree.nodes[case_marker_head]['form'] in obl_words:
                                    obl_words.remove(tree.nodes[case_marker_head]['form'])
                                if tree.nodes[case_marker]['form'] in obl_words:
                                    obl_words.remove(tree.nodes[case_marker]['form'])
                    
                    obl_subtree_dir=[] #driection of subtree of obl
                    for edgex in obl_subtree.edges:
                        if tree.nodes[edgex[1]]['misc'] is not None:
                            misc_column=list(tree.nodes[edgex[1]]['misc'].keys())[0]
                        else:
                            misc_column=None
                        if edgex[0]==obl[v_i_i] and misc_column not in misc_tags:
                            obl_subtree_dir.append(dependency_direction(edgex))

                    obl_direction = 0
                    if len(obl_subtree_dir)==0:
                        obl_direction='No Direction'
                    else:
                        RL=0
                        LR=0
                        for value in obl_subtree_dir:
                            if value =='RL':
                                RL+=1
                            elif value =='LR':
                                LR+=1
                        if RL==LR==0:
                            obl_direction='No Direction'
                        elif RL==LR:
                            obl_direction='Both'
                        elif RL>LR:
                            obl_direction='RL'
                        elif LR>RL:
                            obl_direction='LR'


                    category=0
                    if num_cross(tree, obl[v_i_i], verb_index[v_i_i]) ==0 and num_cross(tree, nsubj[v_i_i], verb_index[v_i_i])==0:
                        if obl[v_i_i]<nsubj[v_i_i]<verb_index[v_i_i]:#Checking crossing for this condition because v is final
                            category='obl_sv'
                        elif obl[v_i_i]<verb_index[v_i_i]<nsubj[v_i_i]:
                            category='obl_vs'
                        elif nsubj[v_i_i]<verb_index[v_i_i]<obl[v_i_i]:
                            category="sv_obl"
                        elif nsubj[v_i_i]<obl[v_i_i]<verb_index[v_i_i]:#Checking crossing for this condition because v is final
                            category='s_obl_v'
                        elif verb_index[v_i_i]<nsubj[v_i_i]<obl[v_i_i]:
                            category='vs_obl'
                        elif verb_index[v_i_i]<obl[v_i_i]<nsubj[v_i_i]:
                            category='v_obl_s'
                    
                    if category!=0:
                        if nsubj_direction==0 or obl_direction==0:
                            print('it is zero')
                        row1=[
                        lang,
                        sent_id,
                        sentence.metadata[Sentence],
                        n+1,
                        category,
                        sum(dd)/len(dd)
                        ]
                        csvwriter1.writerow(row1) #saving 
                        
                        #Character length for nsubj, obj and iobj
                        nsubj_char_len=0
                        for nsubj_word in nsubj_words:
                            char_len = len(nsubj_word.replace(" ",""))
                            nsubj_char_len+=char_len
                        obl_char_len=0
                        for obl_word in obl_words:
                            char_len = len(obl_word.replace(" ",""))
                            obl_char_len+=char_len

                        csvwriter2.writerow([lang,
                                            sent_id,
                                            sentence.metadata[Sentence],
                                            n+1,
                                            category,
                                            sum(dd)/len(dd),
                                            nsubj[v_i_i],
                                            tree.nodes[nsubj[v_i_i]]['form'],
                                            nsubj_words,
                                            len(nsubj_words),
                                            nsubj_char_len,
                                            nsubj_direction,
                                            obl[v_i_i],
                                            tree.nodes[obl[v_i_i]]['form'],
                                            obl_words,
                                            len(obl_words),
                                            obl_char_len,
                                            obl_direction
                                            ])

# directory_dia = "../../Dialouge Corpus Filttered"                    # directory containing the Dialogue corpus tree files in CONLLU format
# fin_nsubj_obl(directory_dia, 'Sentence','nsubj_obl.csv','token_wise_nsubj_obl.csv')

directory_txt="../../UD_Hindi-HDTB"
fin_nsubj_obl(directory_txt, 'text','nsubj_obl_txt.csv','token_wise_nsubj_obl_txt.csv')
