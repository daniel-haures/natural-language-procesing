import nltk
import scipy
import pandas as pd
import numpy as np

import csv
from nltk.corpus import wordnet as wn


#MAX_DEPTH = max(max(len(hyp_path) for hyp_path in ss.hypernym_paths()) for ss in wn.all_synsets())
MAX_DEPTH=20

#Wu & Palmer similarity
def wu_similarity(v1,v2):
    if(v1==v2):
        return 1.0
    lcs , _ = LCS(v1,v2)
    if(not lcs):
        return 0
    wu = (2*(depth(lcs[0])))/(depth(v1)+depth(v2))
    return round(wu,3)


#Shortest Path similarity
def sp_similarity(v1,v2):
    _ , len = LCS(v1,v2)
    if len is None:
        sp=0
    else:
        sp=2*MAX_DEPTH-len
    return sp

#Leak & Chod
#def lch_similarity(v1,v2):

def LCS(s1,s2):
    #SE s1 e s2 sono uguali?
    s1_dict = {str(s1):0}
    s2_dict = {str(s2):0}
    s1_to_expand = [s1]
    s2_to_expand = [s2]
    matches=[]
    level=1
    while not matches and (s1_to_expand or s2_to_expand):
        hyperonism_1=[]
        for s1_ext in s1_to_expand:
            if(str(s1_ext) in s2_dict):
                matches.append(s1_ext)
            else:
                for s1_hypr in s1_ext.hypernyms():
                    s1_dict.update({str(s1_hypr):level})
                    hyperonism_1.append(s1_hypr)
        s1_to_expand=hyperonism_1
    
        hyperonism_2=[]
        for s2_ext in s2_to_expand:
            if(str(s2_ext) in s1_dict):
                matches.append(s2_ext)
            else:
                for s2_hypr in s2_ext.hypernyms():
                    s2_dict.update({str(s2_hypr):level})
                    hyperonism_2.append(s2_hypr)
        s2_to_expand=hyperonism_2

        level+=1
    
    if (len(matches) > 1): #se c'è più di un match allora 
        #min(common_hypernyms, key=lambda x: x.shortest_path_distance(synset1) + x.shortest_path_distance(synset2))
        min=matches[0]
        for actual in matches:
            value_min=s1_dict.get(str(min))+s2_dict.get(str(min))
            value_actual=s1_dict.get(str(actual))+s2_dict.get(str(actual))
            if(value_actual<value_min):
                min=actual
        return [min] , (s1_dict.get(str(min))+s2_dict.get(str(min)))
    elif (len(matches)==1):#se c'è solo un mathc
        return matches , (s1_dict.get(str(matches[0]))+s2_dict.get(str(matches[0])))
    else:
        return [], None

def depth(v1):
    count = 1
    hypernym = v1
    while str(hypernym.hypernyms()) != "[]":
        hypernym = hypernym.hypernyms()[0]
        count=count+1
    return count

tiger=wn.synsets('cock')
cat=wn.synsets('pussy')
#print(tiger)
#print(cat)

print(tiger[0].shortest_path_distance(cat[0]))
_ , spd= LCS(tiger[0],cat[0])
print(spd)



#print(LCS(tiger[1],cat[0]))
#print(tiger[1].lowest_common_hypernyms(cat[0]))


        


