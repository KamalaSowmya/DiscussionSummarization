#Assumptions 1: First sentence will have a keyword, else take the keyword from the question.
#Assumptions 2: Discussion on only one topic at a time
#Assumptions 3: More than one sentence should be there for one topic(it should not be one sentence in one comment pertaining to one discussion)

import nltk
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import LineTokenizer
import math
from linkedlist import LinkedList
from linkedlist import Sentencenode
from linkedlist import Clusternode
from maxSim import maxSim
from theme import Themenode
from theme import ThemeSentencenode
from theme import ThemeLinkedList
from nltk.corpus import wordnet as wn
from stemming.porter2 import stem
from nltk.probability import FreqDist


#array of superstition keywords
superstition=('cat','sneeze','widow')
fil=open("C:\Users\sowmya\Desktop\project\LATEST\pythonpro\MAIN\in0.txt")
inp=fil.read()
#tokenizing word wise
base_words = [word.lower() for word in nltk.word_tokenize(inp)]
#words other than stop words
words = [word for word in base_words if word not in stopwords.words()]
#associated array
word_frequencies = FreqDist(words)
#tokenize sentence wise, stok - array
stok=nltk.sent_tokenize(inp)

print words

def idf(word):
    print word
    return math.log(len(stok)/word_frequencies[word.lower()])
#cosine similarity
def CosSim(a,b):
    cossim=0
    moda=0
    aa= [word for word in a if word not in stopwords.words()]
    bb= [word for word in b if word not in stopwords.words()]
    for i in aa:
       # print "into aa"
	   #sum of square values
        moda=moda + word_frequencies[i]*word_frequencies[i]
    moda=moda**(.5)
    modb=0
    for i in bb:
        #print "into bb"
        modb=modb + word_frequencies[i]*word_frequencies[i]
    modb=modb**(.5)
	#a.b iff equal
    for i in aa:
        for j in bb:
            if(i==j):
                cossim=cossim+(word_frequencies[i]* word_frequencies[j])
    if (moda*modb == 0.0):
        return 0
    else:
        cossim=cossim/(moda*modb)
        return cossim
#above function is for finding similarity between two sentences



#ranking algorithm --- bi-type graph
#w-wieght = cosine similarity values
wss =[]
for i in range (0,len(stok)):
    wss.append([])
    for j in range(0,len(stok)):
        wss[i].append(CosSim(nltk.word_tokenize(stok[i]),nltk.word_tokenize(stok[j])))

wst =[]
for i in range (0,len(stok)):
    wst.append([])
    for j in range(0,len(words)):
        wst[i].append(CosSim(nltk.word_tokenize(stok[i]),nltk.word_tokenize(words[j])))

wts =[]
for i in range (0,len(words)):
    wts.append([])
    for j in range(0,len(stok)):
        wts[i].append(CosSim(nltk.word_tokenize(words[i]),nltk.word_tokenize(stok[j])))

wtt =[]
for i in range (0,len(words)):
    wtt.append([])
    for j in range(0,len(words)):
        wtt[i].append(CosSim(nltk.word_tokenize(words[i]),nltk.word_tokenize(words[j])))


	#initial rank of sentence- rs (number of likes ---to be changed)
rs=[]
for i in range (0,len(stok)):
    sen_word=nltk.word_tokenize(stok[i])
    sen_keyword=[word for word in sen_word if word not in stopwords.words()]
    cc=0
    for j in range(0,len(sen_keyword)):
        cc=cc+word_frequencies[sen_keyword[j]]
    rs.append(cc)

# ranking algo - score of a sentence
def ranking(a,pos):# a- sentence
    rank=0
    for j in range (0,len(words)):
        #rank=rank+ wst[pos][j]*word_frequencies[words[j]]
        rank=rank + wst[pos][j] * idf(words[j])
    for j in range (0,len(stok)):
        rank=rank + wss[pos][j] * rs[j]
    return rank


#Creating the theme cluster
theme=ThemeLinkedList()
key='sneeze'
for a in stok:
    sen_count=0
	#sentence's words which are tokenized
    sen1=nltk.word_tokenize(a)
    for i in sen1:
        for j in superstition:
            #qq=wn.synsets(i)
            #if(contains(wn.synsets(j),qq)):
            print stem(i)
            if(stem(i).lower()==stem(j).lower()):
                key=j #remember the assumption
                print "____________"
                print i
    themename=theme.search(key)
    if(themename!=None):
        theme.addsen(a,sen_count,theme.search(key))
    else:
        theme.add(key,a,sen_count)
    sen_count=sen_count+1

theme.display()


#Creating Similarity cluster
l=LinkedList()
pos_count=0
hash_table={}
#check similarity within a cluster
tempnode=theme.head
while tempnode!=None:
#cluster wise orderly retrieval
    hash_table[tempnode.name]=pos_count
    stok1=theme.retrieveSen(tempnode) #if length(stok1>2) , give tab   ; else add(stok1[0],pos_count) po_count++ ...identation
    pos1=theme.retrievePos(tempnode)
    tempnode=tempnode.next

#l=0
    sim=0
    deno1=0
    deno2=0
    num1=0
    num2=0

    list1=nltk.word_tokenize(stok1[0])
    list2=nltk.word_tokenize(stok1[1])
    l1=len(list1)
    l2=len(list2)
    l1=l1-1
    l2=l2-1
    i=0
	#removal of stop words
    while(i<len(list1)):
         if list1[i].lower() in stopwords.words():
             del list1[i]
             i=i-1
         i=i+1
    i=0
    print(i)
    while(i<len(list2)):
         if list2[i].lower() in stopwords.words():
             del list2[i]
             i=i-1
         i=i+1
    i=0
    l1=len(list1)
    l2=len(list2)
#l1=l1-1
#l2=l2-1
    while(i<l1):
     deno1=deno1+idf(list1[i])
     j=0
     while(j<l2):
         n=0
         f1=0
         f2=0
         if(maxSim(list1[i],list2[j])):
            #n=n+1
            #if((i!=0)&(j!=0)):
             #   f1=maxSim(list1[i-1],list2[j-1])
              #  n=n+1
            #if((i!=(l1-1))&(j!=(l2-1))):
             #   f2=maxSim(list1[i+1],list2[j+1])
              #  n=n+1
            #num1=num1+((1.0+f1+f2)/n)*idf(list1[i])
			num1=num1+idf(list1[i])
         j=j+1
     i=i+1
    i=0
    while(i<l2):
     deno2=deno2+idf(list2[i])
     j=0
     while(j<l1):
         if(maxSim(list2[i],list1[j])):
             n=0
             f1=0
             f2=0
             if(maxSim(list1[j],list2[i])):
               """ n=n+1
                if((i!=0)&(j!=0)):
                    f1=maxSim(list1[j-1],list2[i-1])
                    n=n+1
                if((j!=(l1-1))&(i!=(l2-1))):
                    f2=maxSim(list1[j+1],list2[i+1])
                    n=n+1
             num2=num2+((1.0+f1+f2)/n)*idf(list2[i])"""
             num2=num2+idf(list2[i])
         j=j+1
     i=i+1


    count=0
    sim=0.5*((num1/deno1)+(num2/deno2))
    if(sim>.7): #why .7 ---- Jaccard's
        l.add(stok1[0],pos_count)
        pos_count=pos_count+1
        l.addsen(stok1[1],pos_count,l.search(stok1[0]))
        pos_count=pos_count+1
        count=1
    #print(l.head.child.data)

    else:#two clusters
        l.add(stok1[0],pos_count)
        pos_count=pos_count+1
        l.add(stok1[1],pos_count)
        pos_count=pos_count+1
        count=2
    #print(l.head.child.data)
    #print(l.head.next.child.data)
    #print("aaaaa\n")
    #print(l.head.child.data)


	#match sentences with clusters(recursive)
    ns=len(stok1)
    x=2
    while(x<ns):
        y=0
        temp=l.head
        while(y<count):
            sim=0
            deno1=0
            deno2=0
            num1=0
            num2=0
            list1=nltk.word_tokenize(temp.child.data) #chk the i/p sent with only the first sent of the cluster
            list2=nltk.word_tokenize(stok1[x])
            l1=len(list1)
            l2=len(list2)
            #print(l1)
            #print(l2)
            i=0
            while(i<len(list1)):
                 #print(list1[i].lower())
                 if list1[i].lower() in stopwords.words():
                     #print("hai supriya")
                     #print(list1[i])
                     del list1[i]
                     i=i-1
                 i=i+1
            i=0
            while(i<len(list2)):
                 if list2[i].lower() in stopwords.words():
                     #print(list2[i])
                     del list2[i]
                     i=i-1
                 i=i+1
            i=0
            l1=len(list1)
            l2=len(list2)
            #l1=l1-1
            #l2=l2-1
            while(i<l1):
             deno1=deno1+idf(list1[i])
             j=0
             while(j<l2):
                 n=0
                 f1=0
                 f2=0
                 if(maxSim(list1[i],list2[j])):
                    n=n+1
                    if((i!=0)&(j!=0)):
                        f1=maxSim(list1[i-1],list2[j-1])
                        n=n+1
                    if((i!=(l1-1))&(j!=(l2-1))):
                        f2=maxSim(list1[i+1],list2[j+1])
                        n=n+1
                    #num1=num1+((1.0+f1+f2)/n)*idf(list1[i])
                    num1=num1+(1.0)*idf(list1[i])
                 j=j+1
             i=i+1
            i=0
            while(i<l2):
             deno2=deno2+idf(list2[i])
             j=0
             while(j<l1):
                 if(maxSim(list2[i],list1[j])):
                     n=0
                     f1=0
                     f2=0
                     if(maxSim(list1[j],list2[i])):
                        n=n+1
                        if((i!=0)&(j!=0)):
                            f1=maxSim(list1[j-1],list2[i-1])
                            n=n+1
                        if((j!=(l1-1))&(i!=(l2-1))):
                            f2=maxSim(list1[j+1],list2[i+1])
                            n=n+1
                     #num2=num2+((1.0+f1+f2)/n)*idf(list2[i])
                     num2=num2+(1.0)*idf(list2[i])
                 j=j+1
             i=i+1
            flag=0
            sim=0.5*((num1/deno1)+(num2/deno2))
            if(sim>.7):
                l.addsen(stok1[x],pos_count,temp)
                pos_count=pos_count+1
                flag=1
                break
            else:
                temp=temp.next
            y=y+1
        if(flag==0):
            l.add(stok1[x],pos_count)
            pos_count=pos_count+1

        x=x+1
        #print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
        #hash_table[tempnode.name]=pos_count
        #print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
    #hash_table[tempnode.name]=pos_count

l.display()
for x in hash_table.keys():
    print x
#Ranking the sentences inside the cluster
elig_sent=[]
elig_sent_pos=[]
elig_sent_score=[]
temp_clust=l.head
while (temp_clust != None):
#  twice ranking sentence cluster(only one sentence), inturn similarity cluster.
    temp_sent_clust=temp_clust.child
    max_score=0
    sen_pos=0
    max_sentence="aaa"
    sentence=temp_sent_clust.data
    while (temp_sent_clust != None):
        score=ranking(temp_sent_clust.data,temp_sent_clust.pos)
        if(score > max_score):
            max_score=score
            max_sentence=temp_sent_clust.data
            sen_pos=temp_sent_clust.pos

        temp_sent_clust=temp_sent_clust.next
       # elig_sent = max scored ones across all clusters
    elig_sent.append(max_sentence)
    elig_sent_score.append(max_score)
    elig_sent_pos.append(sen_pos)
    temp_clust=temp_clust.next

#print all elig_sent
for i in range(0,len(elig_sent)):
    print elig_sent[i]
#highly ranked sentences in each similar cluster available
#sort the sentences

for i in range(0,len(elig_sent)):
    for j in range(i+1,len(elig_sent)):
        if (elig_sent_score[i]<elig_sent_score[j]):
		#score, position and sentence are sorted
            t_sen=elig_sent[i]
            elig_sent[i]=elig_sent[j]
            elig_sent[j]=t_sen

            t_score=elig_sent_score[i]
            elig_sent_score[i]=elig_sent_score[j]
            elig_sent_score[j]=t_score

            t_pos=elig_sent_pos[i]
            elig_sent_pos[i]=elig_sent_pos[j]
            elig_sent_pos[j]=t_pos

#reorder the sentences
n=2
if(n>len(elig_sent)):  # make it dynamic
   n=elig_sent
for i in range(0,n):
# sort according to the position
    for j in range(i+1,n):
        if(elig_sent_pos[i]>elig_sent_pos[j]):
            t_sen=elig_sent[i]
            elig_sent[i]=elig_sent[j]
            elig_sent[j]=t_sen

            t_score=elig_sent_score[i]
            elig_sent_score[i]=elig_sent_score[j]
            elig_sent_score[j]=t_score

            t_pos=elig_sent_pos[i]
            elig_sent_pos[i]=elig_sent_pos[j]
            elig_sent_pos[j]=t_pos

for k in elig_sent:
    print k

#displaying the summary
print "---------------------summary----------------------------"
j=0
hash_table["end"]=10000
key_names=[] # all key value in hash table
for k in hash_table.keys():
    key_names.append(k)


i=len(key_names)-1
while (i >0):
    print key_names[i]
    for k in range(j,n):
	#positioning of a sentence
        if(hash_table[key_names[i-1]]<=elig_sent_pos[k]):
            #j=j-1
            break
        print elig_sent[k]
        #print elig_sent_pos[k]
        j=j+1
    i=i-1


