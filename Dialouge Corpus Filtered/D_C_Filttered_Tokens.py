#Filtering the data on the bases of following arguments


import os
import csv
from conllu import parse

#Input conllu format files
#Directory sequence : parse_gold/Phase1/Phase1_gold/hi_xxxx_gold.conllu\

#Output conllu format files
#Directory sequence : parse_gold_filttered/Phase1/hi_xxxx_filttered.conllu

def Filter_DC(filepath_in, filepath_out, tag_list):
    #Parameters
    #filename_in : Input File path
    #file_path_out : Output File path
    #tag_list: list of tags needed to be removed
    #  
    dir = sorted(os.listdir(filepath_in))
    # print(dir)
    # for phase_dir in dir:
    #     print(phase_dir)
    #     # if not os.path.isfile(filepath_in+"/"+str(phase_dir)):
    #     phase_gold_dir = phase_dir   # Accessing output files folder in each phase
    #     print(phase_gold_dir)
    for phase in dir:
        if not os.path.isfile(filepath_in+"/"+str(phase)):
            output_files_dir = sorted(os.listdir(filepath_in+"/"+str(phase)))
            for output_file in output_files_dir:
                print(output_file)
                filename = filepath_in+"/"+str(phase)+"/"+str(output_file)    # Looping over each output file in output files folder
                if filename.endswith(".conllu"):
                    data_file = open(str(filename),'r',encoding='utf-8').read()
                    file1 = parse(data_file)       # Loading CoNLL output file using pyconll module
                    # print(len(file1))
                    for sentence in file1:
                        t_i=0
                        while t_i < len(sentence):
                            if sentence[t_i]['misc'] != None:
                                List_Misc = list(sentence[t_i]['misc'].keys())
                            else:
                                List_Misc = ['None']
                            if str(sentence[t_i]).strip() in tag_list or 'Hesitation' in List_Misc or 'Disfluency' in List_Misc or 'Repair' in List_Misc:
                                sentence.metadata['Sentence'] = sentence.metadata['Sentence'].replace(str(sentence[t_i])+' ','')
                                token_id_del =sentence[t_i]['id']
                                # del sentence[t_i]
                                for t_i_del in range(token_id_del, len(sentence)):
                                    sentence[t_i_del]['id']=sentence[t_i_del]['id']-1
                                    for t_i_new in range(0, len(sentence)):
                                        if sentence[t_i_new]['head'] == sentence[t_i_del]['id']:
                                            sentence[t_i_new]['head']=sentence[t_i_new]['head']-1
                                del sentence[t_i]
                                t_i+=2
                            else:
                                t_i+=1
                        if sentence.metadata['sent_id'] == '22':
                            print(sentence)
                    filename_out = filepath_out+"/"+str(phase)+"/"+str(output_file)
                    with open(filename_out, 'w', encoding = 'utf-8') as f:
                        f.writelines([sentence.serialize() + "\n" for sentence in file1])

tag_list_to_be_removes=['[noise]','[laughter]','[aside]','[b_aside]','[e_aside]','[pause]']
Filter_DC('./parse_gold_filttered/Phase3', './parse_gold_filttered/Phase3', tag_list_to_be_removes)