# DLM-in-naturalistic-dialogue

"Data_Dialogue" consist of baselines generated from Hindi Dialogue Corpus.
"Data_Text" consist of baselines generated from HDTB.
 For more information on how to generate baselines please refer to following citation:
Himanshu Yadav, Shubham Mittal, Samar Husain; A Reappraisal of Dependency Length Minimization as a Linguistic Universal. Open Mind 2022; 6 147–168. doi: https://doi.org/10.1162/opmi_a_00060


"Dialogue Corpus Filtered" consist of python code to filter the Hindi Dialogue Corpus. Filtering criteria is mentioned in the readme inside the folder

"Measures" consist of code to calculate dependency length, dependency direction, number of crossings. This code is used in other programs.

"graphs" consist of graphs obtained from the Analysis

Section 2 DLM during dialogue and Section 4 DLM in speech vs written text:<br />
"DLM_during_dialogue and DLM in speech vs written text" is for the analysis of dependency length minimisation in Dialogue Cropus and Speech Vs Written text analysis<br />

Section 3 What drives DLM?:<br />
3.1 Long-before-short order: "Long Before Short" is to recognise and analyse long before short order for arguments and adjuncts.<br />
3.2 Right-extraposition: "Right Extraposition" is to collect non project instances and analyse them.<br />

They all consists of:
1. a python file to compute the numbers from raw baseline data
2. Rmd file which shows the analysis and model fitting
3. pdf file obtained from the rmd file which shows the data structure and model output
4. Output of the python file

For more details about the project and pre-print of the paper go to https://osf.io/vxd6w/
