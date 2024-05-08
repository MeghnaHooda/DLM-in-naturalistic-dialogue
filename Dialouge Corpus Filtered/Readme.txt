D_C_Filterred script follow the following criteria's from the Hindi Dialogue Corpus.

Include: expletive, anonymized (Do no remove)

Exclude complete sentences: if code switch (more than one word); quotation; incomprehensible

Exclude only token: hesitation, disfluency, repair, pause, noise, laughter, aside, easide, baside

For D_C_Filterred_Sentence

Exclude complete sentences: if code switch (more than one word); quotation; incomprehensible from gold_data

Input conllu format files
Directory sequence : parse_gold/Phase1/Phase1_gold/hi_xxxx_gold.conllu

Output conllu format files
Directory sequence : parse_gold_filttered/Phase1/hi_xxxx_filttered.conllu


For D_C_Filterred_Token

Exclude only token: hesitation, disfluency, repair, pause, noise, laughter,aside, easide, baside form the sentences and changing
the token id. Take data form the filtered data from above step and include form it.

Input conllu format files
Directory sequence : parse_gold_filttered/Phase1/hi_xxxx_filttered.conllu

Output conllu format files
Directory sequence : parse_gold_filttered/Phase1/hi_xxxx_filttered.conllu

For complete filtering criteria:
first run For D_C_Filterred_Sentence and then For D_C_Filterred_Token