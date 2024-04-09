import nltk
import scipy
import pandas as pd
import numpy as np

import csv
from nltk.corpus import wordnet as wn


#Wu & Palmer similarity
def wu_similarity(v1,v2):
    if(v1==v2):
        return 1.0
    lcs = LCS(v1,v2)
    if(not lcs):
        return 0
    wu = (2*(lcs[0].max_depth()+1))/(v1.max_depth()+v2.max_depth()+2)
    return round(wu,3)


#Shortest Path similarity
#def sp_similarity(v1,v2):

#Leak & Chod
#def lch_similarity(v1,v2):

def LCS(s1,s2):
    s1_set = {str(s1)}
    s2_set = {str(s2)}
    s1_to_expand = [s1]
    s2_to_expand = [s2]
    matches=[]
    while not matches and (s1_to_expand or s2_to_expand):
        for s1_ext in s1_to_expand:
            if(str(s1_ext) in s2_set):
                matches.append(s1_ext)#DA METTERE FUORI DAL FOR
            else:
                for s1_hypr in s1_ext.hypernyms():
                    s1_set.add(str(s1_hypr))
                    s1_to_expand.append(s1_hypr)#DA METTERE FUORI DAL FOR
            s1_to_expand.remove(s1_ext)#DA METTERE FUORI DAL FOR
    
    
        for s2_ext in s2_to_expand:
            if(str(s2_ext) in s1_set):
                matches.append(s2_ext)#DA METTERE FUORI DAL FOR
            else:
                for s2_hypr in s2_ext.hypernyms():
                    s2_set.add(str(s2_hypr))
                    s2_to_expand.append(s2_hypr)#DA METTERE FUORI DAL FOR
            s2_to_expand.remove(s2_ext)#DA METTERE FUORI DAL FOR
    
    if (matches):
        #min(common_hypernyms, key=lambda x: x.shortest_path_distance(synset1) + x.shortest_path_distance(synset2))
        min=matches[0]
        for actual in matches:
            value_min=s1.shortest_path_distance(min) + s2.shortest_path_distance(min)
            value_actual=s1.shortest_path_distance(actual) + s2.shortest_path_distance(actual)
            if(value_actual<value_min):
                min=actual
        return [min]
    else:
        return []
    

tiger=wn.synsets('weather')
cat=wn.synsets('forecast')
print(tiger)
print(cat)

for s1 in tiger:
    for s2 in cat:
        print(LCS(s1,s2))
        print(s1.lowest_common_hypernyms(s2))


