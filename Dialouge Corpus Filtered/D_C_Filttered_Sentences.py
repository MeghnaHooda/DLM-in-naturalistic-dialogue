#Filtering the data on the bases of following arguments


import os
import csv
from conllu import parse

#Input conllu format files
#Directory sequence : parse_gold/Phase1/Phase1_gold/hi_xxxx_gold.conllu\

#Output conllu format files
#Directory sequence : parse_gold_filttered/Phase1/hi_xxxx_filttered.conllu

def Filter_DC(filepath_in, filepath_out):
    #Parameters
    #filename_in : Input File path: The Corpus Data
    #file_path_out : Output File path : The filttered Data
    #tag_list: list of tags needed to be removed
    #  
    dir = sorted(os.listdir(filepath_in))
    # print(dir)
    for phase_dir in dir:
        # print(phase_dir)
        if not os.path.isfile(filepath_in+"/"+str(phase_dir)):
            phase_gold_dir = sorted(os.listdir(filepath_in+"/"+str(phase_dir)))   # Accessing output files folder in each phase
            # print(phase_gold_dir)
            for phase in phase_gold_dir:
                if not os.path.isfile(filepath_in+"/"+str(phase_dir)+"/"+str(phase)):
                    output_files_dir = sorted(os.listdir(filepath_in+"/"+str(phase_dir)+"/"+str(phase)))
                    for output_file in output_files_dir:
                        print(output_file)
                        filename = filepath_in+"/"+str(phase_dir)+"/"+str(phase)+"/"+str(output_file)    # Looping over each output file in output files folder
                        if filename.endswith(".conllu"):
                            data_file = open(str(filename),'r',encoding='utf-8').read()
                            file1 = parse(data_file)       # Loading CoNLL output file using pyconll module
                            # print(file1)
                            s_i=0
                            while s_i < len(file1):
                                sentence = file1[s_i]
                                t_i=0
                                while t_i < len(sentence):
                                    if sentence[t_i]['misc'] != None:
                                        List_Misc = list(sentence[t_i]['misc'].keys())
                                        if 'CodeSwitch' in List_Misc:
                                            sentence_unpack=str(sentence[t_i]['form']).split('_')
                                            if len(sentence_unpack)>1:
                                                file1.pop(s_i)
                                                t_i+=1
                                                s_i-=1
                                                continue
                                        elif 'Quote' in List_Misc or sentence[t_i]=='[incomprehensible]':
                                            file1.pop(s_i)
                                            t_i+=1
                                            s_i-=1
                                            continue
                                    t_i+=1
                                s_i+=1
                            filename_out = filepath_out+"/"+str(phase_dir)+"/"+str(output_file)
                            with open(filename_out, 'w', encoding = 'utf-8') as f:
                                f.writelines([sentence.serialize() + "\n" for sentence in file1])
                                    # if str(sentence[t_i]) in tag_list:
                            #             sentence.metadata['Sentence'] = sentence.metadata['Sentence'].replace(str(sentence[t_i])+' ','')
                            #             token_id_del =sentence[t_i]['id']
                            #             # del sentence[t_i]
                            #             for t_i_del in range(token_id_del, len(sentence)):
                            #                 sentence[t_i_del]['id']=sentence[t_i_del]['id']-1
                            #                 for t_i_new in range(0, len(sentence)):
                            #                     if sentence[t_i_new]['head'] == sentence[t_i_del]['id']:
                            #                         sentence[t_i_new]['head']=sentence[t_i_new]['head']-1
                            #             del sentence[t_i]
                            #             t_i+=2
                            #         else:
                            #             t_i+=1
                            # filename_out = filepath_out+"/"+str(phase_dir)+"/"+str(output_file)
                            # with open(filename_out, 'w', encoding = 'utf-8') as f:
                            #     f.writelines([sentence.serialize() + "\n" for sentence in file1])

Filter_DC('./Phase3_partial_Data', './parse_gold_filttered')