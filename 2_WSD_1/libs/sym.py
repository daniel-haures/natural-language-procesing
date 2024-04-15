import nltk
import scipy
import pandas as pd
import numpy as np
import math
import csv
from nltk.corpus import wordnet as wn


#MAX_DEPTH = max(depth(ss) for ss in wn.all_synsets())
MAX_DEPTH=19

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

#Leak & Chod similarity
def lch_similarity(v1,v2):
    _ , len = LCS(v1,v2)
    lch=0
    if len is None:
        lch=0
    elif (len==0):
        lch=math.log10((2*MAX_DEPTH+1))
    else:
        lch=-math.log10((len)/(2*MAX_DEPTH))
    return lch

#returns the lcs and shortest path of two synset
def LCS(s1,s2):
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
    
    if (len(matches) > 1): 
        lcs = min(matches, key=lambda x: s1_dict.get(str(x)) + s2_dict.get(str(x)))
        return [lcs] , (s1_dict.get(str(lcs))+s2_dict.get(str(lcs)))
    
    elif (len(matches)==1):
        return matches , (s1_dict.get(str(matches[0]))+s2_dict.get(str(matches[0])))
    
    else:
        return [], None

#return the maximum depth from root to v1
def depth(v1):
    count = 1
    hypernym = v1
    while str(hypernym.hypernyms()) != "[]":
        hypernym = hypernym.hypernyms()[0]
        count=count+1
    return count


        


