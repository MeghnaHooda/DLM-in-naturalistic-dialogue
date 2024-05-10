# Making a distribution of same number of files controlling for sentence lnegth, max arity and max HDD in Dialogue and Text RLA Baseline
import pandas as pd
import random

def equal_dist_dialogue_written(dialogue_baseline, text_baseline):
    baseline_RLA_dialogue = pd.read_csv(dialogue_baseline)
    # print(baseline_RLA_dialogue.head)
    baseline_RLA_text = pd.read_csv(text_baseline)
    # print(baseline_RLA_text.head)

    column_names=["lang","dtype","sent_id","length","avg_arity","max_arity","projD","maxHD","avgDD","Genre"]
    new_combined_df = pd.DataFrame(columns=column_names)
    # new_combined_df=pd.concat([new_combined_df, baseline_RLA_dialogue.loc[[0],column_names]], ignore_index=True)

    unique_sent_length = baseline_RLA_dialogue["length"].unique()
    print(unique_sent_length)
    for sent_length in unique_sent_length:
        # print("length",sent_length)
        baseline_RLA_dialogue_sent_id = baseline_RLA_dialogue.loc[(baseline_RLA_dialogue["length"]==sent_length) & (baseline_RLA_dialogue["dtype"]=='real')]
        baseline_RLA_text_sent_id = baseline_RLA_text.loc[(baseline_RLA_text["length"]==sent_length) & (baseline_RLA_text["dtype"]=='real')]

        unique_max_arity = baseline_RLA_dialogue_sent_id["max_arity"].unique()
        for max_arity in unique_max_arity:
            # print("arity",max_arity)
            baseline_RLA_dialogue_sent_id_max_arity=baseline_RLA_dialogue_sent_id.loc[(baseline_RLA_dialogue_sent_id["max_arity"]==max_arity) & (baseline_RLA_dialogue["dtype"]=='real')]
            baseline_RLA_text_sent_id_max_arity=baseline_RLA_text_sent_id.loc[(baseline_RLA_text_sent_id["max_arity"]==max_arity) & (baseline_RLA_text["dtype"]=='real')]
            unique_max_hd = baseline_RLA_dialogue_sent_id_max_arity["maxHD"].unique()
            for max_hd in unique_max_hd:
                # print("HD",max_hd)
                baseline_RLA_dialogue_sent_id_max_arity_max_hd=baseline_RLA_dialogue_sent_id_max_arity.loc[(baseline_RLA_dialogue_sent_id_max_arity["maxHD"]==max_hd) & (baseline_RLA_dialogue["dtype"]=='real')]
                baseline_RLA_text_sent_id_max_arity_max_hd=baseline_RLA_text_sent_id_max_arity.loc[(baseline_RLA_text_sent_id_max_arity["maxHD"]==max_hd) & (baseline_RLA_text["dtype"]=='real')]
                num_dia = len(baseline_RLA_dialogue_sent_id_max_arity_max_hd)
                num_txt = len(baseline_RLA_text_sent_id_max_arity_max_hd)
                if num_txt!=0 and num_dia!=0:
                    # print(num_dia, num_txt)
                    if num_dia>num_txt:
                        uploaded_index=[]
                        for i in baseline_RLA_text_sent_id_max_arity_max_hd.index:
                            #adding text data to file
                            new_combined_df=pd.concat([new_combined_df, baseline_RLA_text_sent_id_max_arity_max_hd.loc[[i],column_names]], ignore_index=True)
                            #adding its corrsponding random tree
                            # sent_id_temp=baseline_RLA_text_sent_id_max_arity_max_hd.loc[[i],column_names].iloc[0,2]
                            # random_tree_text = baseline_RLA_text.loc[(baseline_RLA_text["sent_id"]==sent_id_temp) & (baseline_RLA_text["dtype"]=="random")]
                            # new_combined_df=pd.concat([new_combined_df, random_tree_text.loc[[random_tree_text.index[0]],column_names]], ignore_index=True)
                            
                            list_dia = list(baseline_RLA_dialogue_sent_id_max_arity_max_hd.index)
                            uploaded=True
                            while uploaded:
                                random_choice=random.choice(list_dia)
                                if random_choice not in uploaded_index:
                                    new_combined_df=pd.concat([new_combined_df, baseline_RLA_dialogue_sent_id_max_arity_max_hd.loc[[random_choice],column_names]], ignore_index=True)
                                    sent_id_temp=baseline_RLA_dialogue_sent_id_max_arity_max_hd.loc[[random_choice],column_names].iloc[0,2]
                                    lang_temp=baseline_RLA_dialogue_sent_id_max_arity_max_hd.loc[[random_choice],column_names].iloc[0,0]
                                    random_tree_dia = baseline_RLA_dialogue.loc[(baseline_RLA_dialogue["sent_id"]==sent_id_temp) & (baseline_RLA_dialogue["lang"]==lang_temp) & (baseline_RLA_dialogue["dtype"]=="random")]
                                    new_combined_df=pd.concat([new_combined_df, random_tree_dia.loc[[random_tree_dia.index[0]],column_names]], ignore_index=True)
                                    uploaded_index.append(random_choice)
                                    uploaded=False
                    elif num_txt>num_dia:
                        uploaded_index=[]
                        for i in baseline_RLA_dialogue_sent_id_max_arity_max_hd.index:
                            new_combined_df=pd.concat([new_combined_df, baseline_RLA_dialogue_sent_id_max_arity_max_hd.loc[[i],column_names]], ignore_index=True)
                            # sent_id_temp=baseline_RLA_dialogue_sent_id_max_arity_max_hd.loc[[i],column_names].iloc[0,2]
                            # lang_temp=baseline_RLA_dialogue_sent_id_max_arity_max_hd.loc[[i],column_names].iloc[0,0]
                            # random_tree_dia = baseline_RLA_dialogue.loc[(baseline_RLA_dialogue["sent_id"]==sent_id_temp) & (baseline_RLA_dialogue["lang"]==lang_temp) & (baseline_RLA_dialogue["dtype"]=="random")]
                            # new_combined_df=pd.concat([new_combined_df, random_tree_dia.loc[[random_tree_dia.index[0]],column_names]], ignore_index=True)

                            list_txt = list(baseline_RLA_text_sent_id_max_arity_max_hd.index)
                            uploaded=True
                            while uploaded:
                                random_choice=random.choice(list_txt)
                                if random_choice not in uploaded_index:
                                    new_combined_df=pd.concat([new_combined_df, baseline_RLA_text_sent_id_max_arity.loc[[random_choice],column_names]], ignore_index=True)
                                    sent_id_temp=baseline_RLA_text_sent_id_max_arity.loc[[random_choice],column_names].iloc[0,2]
                                    random_tree_txt = baseline_RLA_text.loc[(baseline_RLA_text["sent_id"]==sent_id_temp) & (baseline_RLA_text["dtype"]=="random")]
                                    new_combined_df=pd.concat([new_combined_df, random_tree_txt.loc[[random_tree_txt.index[0]],column_names]], ignore_index=True)
                                    uploaded_index.append(random_choice)
                                    uploaded=False
    # print(new_combined_df)
    new_combined_df.to_csv('new_combined_out_2.csv', index=False)
dialogue_baseline = "../Data_Dialouge/Phase123_wo_tag_dis/RLAs_grouped_2.csv"
text_baseline = "../Data_Text/RLAs_grouped_2.csv"

equal_dist_dialogue_written(dialogue_baseline, text_baseline)
