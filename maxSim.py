import nltk
from nltk.tokenize import LineTokenizer
from nltk.corpus import wordnet as wn
import math

def maxSim(a,b):
    flag=0
    if(a==b):
        flag=1
    else:
        seta=wn.synsets(a)
        setb=wn.synsets(b)
        for a in seta:
            for b in setb:
                if(a==b):
                    flag=1
                    break
            if(flag==1):
               break
    
    
    return flag
    
    
