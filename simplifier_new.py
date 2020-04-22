# -*- coding: utf-8 -*-
"""
Created on Fri May 31 17:45:08 2019

@author: hp
"""

import nltk
from nltk.tree import ParentedTree
from nltk.parse import stanford
#from nltk.parse.stanford import StanfordDependencyParser as sdp
parser1 = stanford.StanfordParser()
import SBAR#from nltk.parse.stanford import StanfordDependencyParser as sdp
from nltk.parse.stanford import StanfordParser as sp
#os.environ['CLASSPATH']="F:\\Anaconda3\\NLP\\stanford-parser-full-2018-02-27;C:\\Users\\hp\\AppData\\Roaming\\nltk_data\\taggers\\averaged_perceptron_tagger;F:\\Anaconda3\\NLP\\stanford-ner-2015-12-09"
#For nltk tagger
'''
os.environ['CLASSPATH']="F:\\Anaconda3\\NLP\\stanford-parser-full-2018-02-27;F:\\Anaconda3\\NLP\\stanford-postagger-full-2015-12-09;F:\\Anaconda3\\NLP\\stanford-ner-2015-12-09"
os.environ['STANFORD_MODELS']="F:\\Anaconda3\\NLP\\stanford-ner-2015-12-09\\classifiers;F:\\Anaconda3\\NLP\\stanford-postagger-full-2015-12-09\\models"
os.environ['JAVA_HOME']="C:\\Program Files\\Java\\jdk1.8.0_181\\bin"
'''
parser=sp()
'''
To traverse thru the tree check the tree first then go on using tree[0][1][1]....[0 or 1] depending
 on deepest part of tree.tree[0](first 0 is fixed) then if we print(tree[0][0]) here we get 'Ram' as output
 and tree[0][1] gives rest part of tree.
 '''
import re

from anytree import NodeMixin, Node,AnyNode,RenderTree
#from nltk.parse.stanford import StanfordParser
'''
sentence = "Bag A contains 3 white and 2 blue marbles."
sent1='Ram has two apples and five bananas'
sent2='Ram and Shyam are two brothers'
sent3='Ram is a boy and Sita is a girl.'
sent4='Ram is a boy who is six years old .'
sent5='Ram eats a banana and an apple but sings a song'
sent6='He washed cars over the weekend and now has 86 dollars.'
sent7='While playing piano Ram is singing a song in a room and Shyam is playing violin.'
sent8='Are you kidding, or are you damn serious?'#wrong
sent9='You are a boy, and Sita is a girl'
sent10='Ram sold 6 balls at 10 a.m and 7 balls at 11 a.m .'
sent11='The restaurant sold 6 slices of pie during the day and 7 slices of pie during the night.'
sent12="Sam's dad gave Sam 39 nickels and 31 quarters ."
sent13="Park workers will plant 41 dogwood trees today and 20 dogwood trees tomorrow ."
sent14="How many dogwood trees will the park have when the workers are finished?"#wrong
sent15="Dan picked 9 limes and gave Sara 4 of the limes ."
sent16="This year Diane bought some new hives and increased Diane's honey harvest by 6085 pounds ."
sent17="By the time the ship is fixed 49952 tons of grain would have spilled into the water ."#wrong
sent18="Sara had 4 quarters and 8 dimes in Sara's bank ."
sent19="Mike found 6 seashells and 4 starfishes but 4 of the seashells were broken ."
sent20="Jessica grew 35 watermelons and 30 carrots but the rabbits ate 27 watermelons ."
sent21="Park workers had to cut down 13 walnut trees that were damaged ."#wrong
sent22="Dan bought a clarinet for $ 130.30 , and a song book which was $ 11.24 ."
sent23="Melanie bought a Batman game for $ 6.95, a strategy game for $ 7.90 and a Superman game for $ 7.73 ."
sent24="There are 2 maple trees and 5 popular trees currently in the park ."
sent25="Dan 's cat had kittens and 5 had spots ."
sent26="This year, 712261 male salmon and 259378 female salmon, returned to their rivers ."
sent27="Each day , the polar bear at Richmond 's zoo eats 0.2 bucket of trout and 0.4 bucket of salmon ."
sent28="While eating food and drinking water Ram is singing a song."
sent29='He is eating food and she is playing and they are fighting'
sent30='Ram is playing guitar while talking to Sita.'
sent31='He is playing and she is crying but they are singing.'
sent32='While eating food Ram is singing a song .'
sent33='After she ate the cake , Emma visited Tony in his room .'
'''
split = []
simple_sent=[]
index=[]
index1=0
n=0
but=0
scount=0   
parts = []
ht_3_last_obj = []

#print(pos_tagged)
#SBAR functions start here
def make_tree_sbar(tree,t,sent_list):
    #this fn. converts nltk tree to anytree
    if tree not in sent_list:
        ttt=AnyNode(id=str(tree.label()),parent=t)
        for tt in tree:
            make_tree_sbar(tt,ttt,sent_list)
    else:
        AnyNode(id=str(tree),parent=t)            

def find_sbar(t):
    if t.id=='SBAR':
        global sbar
        sbar=t
    for tt in t.children:
        find_sbar(tt)
def find_vp_in_sbar(t):
    if t.id=='VP':
        global vp_sbar
        vp_sbar=t
    for tt in t.children:
        find_vp_in_sbar(tt)
def find_vp(t):
    if t.id=='SBAR':
        return 
    global f
    if t.id=='VP' and f==True:
        global vp
        vp=t
        f=False
    for tt in t.children:
        find_vp(tt)
def find_np(t):
    if t.id=='SBAR':
        return
    global f
    if t.id=='NP' and f==True:
        global np
        np=t
        f=False
    for tt in t.children:
        find_np(tt)    
def find_vbz(t):
    if t.id=='SBAR':
        return
    global f
    if t.id=='VBZ' and f==True:
        global vbz
        vbz=t.children[0].id
        f=False
    for tt in t.children:
        find_vbz(tt)
def make_sent(t):
    global simple_sentences
    if t.id in sent_list:
        simple_sentences[-1].append(t.id)
    for tt in t.children:
        make_sent(tt)
                
#SBAR functions end here
#Multiple CC functions start here
def pos_tag(tokenized_sent):
    return nltk.pos_tag(tokenized_sent)
    
def has_conj(tagged_sent):
    cc_list = [('and', 'CC'), ('but', 'CC')]
    for cc_pair in cc_list:
        if cc_pair in tagged_sent:
            return True   
    return False
    
def split_needed(sent_list):
    for sent in sent_list:
        if has_conj( pos_tag(tokenize(sent)) ):
            return True
    return False
    
def split(sent, cc_tuple):
    parser = stanford.StanfordParser()
    pos_tagged = pos_tag(tokenize(sent)) 
    tree = next(parser.tagged_parse(pos_tagged)) 
    tree1 = ParentedTree.convert(tree)
#tree.draw()
    count=0
    m=0
    for t in tree1.subtrees():
        if t.label()=='PP':
            count=count+1
    
    index=[]
    index1=0
    if count>0 and (('to') not in tokenized_sent and ('washed') not in tokenized_sent) and (tokenized_sent.count(",")<2):
        for i in range(len(pos_tagged)-3):
            if (pos_tagged[i][1]=='VBD' or pos_tagged[i][1]=='VBZ') and pos_tagged[i+1][1]!='VBG' and pos_tagged[i+3][1]!='CC' and pos_tagged[i+1][1]!='NNP' and pos_tagged[i-1][1]!='CC':
                pos_tagged.insert(i+1,(',',','))
            
        
        for j in range(len(pos_tagged)):
            if pos_tagged[j][1]=='CC':
                index.append(j)
        
    
    for t in tree1.subtrees():
        if t.label()=='SBAR':
            m=m+1
    if len(index)>0 and count>0 and m==0:
        c=0
        for i in range(len(index)):
            pos_tagged.insert(index[i]+c,(',',','))
            c=c+1
    if m>0:
        for j in range(len(pos_tagged)):
            if pos_tagged[j][1]=='CC':
                index1=j 
    
    if (index1>0 and m>0) and count==0:
        pos_tagged.insert(index1,(' ,',','))# ', 'is used
        pos_tagged.insert(index1+2,(', ',','))#' ,' is used
#print(pos_tagged)
    tree = next(parser.tagged_parse(pos_tagged)) 
    p_tree = ParentedTree.convert(tree)
    
    leaf_values = p_tree.leaves()
    parts = []
    ht_3_last_obj = []
        
    if cc_tuple in pos_tagged:
        leaf_index = leaf_values.index(cc_tuple[0])
        tree_location = p_tree.leaf_treeposition(leaf_index)
        parent = p_tree[tree_location[:-2]]
        #print(parent.height())

        if parent.height() == 3:
            # find the noun being referred to
            for subtree in reversed(list(parent.subtrees())):
                if subtree.parent() == parent:
                    if subtree.label() == 'NN' or subtree.label() == 'NNS':
                        ht_3_last_obj = subtree.leaves() + ht_3_last_obj
                        del p_tree[subtree.treeposition()]
            #print("ht 3 last obj -> ", ht_3_last_obj)
            part = []
            for subtree in reversed(list(parent.subtrees())):
                if subtree.parent() == parent:
                    # print(subtree)
                    if subtree.label() != ',' and subtree.label() != 'CC':
                        part = subtree.leaves() + part
                    else:
                        parts.append(part + ht_3_last_obj)
                        part = []
                    del p_tree[subtree.treeposition()]
            parts.append(part + ht_3_last_obj)
            #print('parent', parent)
            #print('treeloc', tree_location)
            parent.append(ParentedTree('INSRT', ['*']))

        else:
            for subtree in reversed(list(parent.subtrees())):
                if subtree.parent() == parent:
                    # print(subtree)
                    if subtree.label() != ',' and subtree.label() != 'CC':
                        parts.append(subtree.leaves() + ht_3_last_obj)
                    del p_tree[subtree.treeposition()]
            #print('parent', parent)
            #print('treeloc', tree_location)
            parent.append(ParentedTree('INSRT', ['*']))
        
    #p_tree.draw()
    #print(parts)


    split = []
    rem = p_tree.leaves()
    start_idx = rem.index('*')

    for part in reversed(parts):
        offset = start_idx
        r_clone = rem.copy()
        del r_clone[offset]
        for i, word in enumerate(part):
            r_clone.insert(offset + i, word)
        split.append(r_clone)

    #print("split", split)
    
    split = [" ".join(sent) for sent in split]
    
    return split
    
def split_util(sent):
    cc_list = [('and', 'CC'), ('but', 'CC')]
    for cc_pair in cc_list:
        if cc_pair in pos_tag(tokenize(sent)):
            return split(sent, cc_pair)   
    return sent
        
    
def rem_dup(list):
    final = []
    for item in list:
        if item not in final:
            final.append(item)
    return final

def simplify(sent):
    initial = [sent]
    final = []
    
    while ( split_needed(initial) ):
        final = []
        while (initial):
            sent = initial.pop(0)
            if (split_needed([sent])):
                for split_sent in reversed(split_util(sent)):
                    final.append(split_sent)
            else:
                final.append(sent)
        #print("final -> ", final)
        initial = final.copy()
    
    final = rem_dup(final)
    final = list(reversed(final))
    #print(final)
    
    return final

def tokenize(sent):
    tokenized_sent=nltk.word_tokenize(sent)
    if ('If') in tokenized_sent and ('then') in tokenized_sent:
        tokenized_sent.remove('If')
        tokenized_sent.insert(tokenized_sent.index('then'),'and')
        tokenized_sent.remove('then')
    if ('because') in tokenized_sent:
        tokenized_sent.insert(tokenized_sent.index('because'),(','))# ', 'is used
        tokenized_sent.insert(tokenized_sent.index('because')+1,(','))
        tokenized_sent.insert(tokenized_sent.index('because'),'and')
        tokenized_sent.remove('because')
    if ('while') in tokenized_sent:
        tokenized_sent.insert(tokenized_sent.index('while'),'and')
        tokenized_sent.remove('while')
    if ('which') in tokenized_sent:
        tokenized_sent.insert(tokenized_sent.index('which'),'and')
        tokenized_sent.remove('which')
    if ('or') in tokenized_sent:
        tokenized_sent.insert(tokenized_sent.index('or'),'and')
        tokenized_sent.remove('or')
    if ('who') in tokenized_sent:
        while (',') in tokenized_sent:
            tokenized_sent.insert(tokenized_sent.index(','),'and')
            tokenized_sent.remove(',')
        tokenized_sent.insert(tokenized_sent.index('who'),'and')
        tokenized_sent.remove('who')
        
    return tokenized_sent
    


with open("All_types_of_inputs.txt","r") as f:
    paragraph=f.read()
sentences = nltk.sent_tokenize(paragraph)
for sentence in sentences:
    print(sentences.index(sentence)),
    print("ComplexSentence: "+sentence)
    tokenized_sent = tokenize(sentence)
    #print(tokenized_sent)

#parse_trees = parser1.tagged_parse(pos_tagged)

    pos_tagged = pos_tag(tokenized_sent)
    parse_trees = parser.tagged_parse(pos_tagged)
    tree = next(parse_trees)
    p_tree = ParentedTree.convert(tree)
    #p_tree.draw()
   
    leaf_values = p_tree.leaves()
# print(leaf_values)
    for i in pos_tagged:
        if ('and') in i:
            n=n+1

        
        if ('but') in i:
            but=but+1
    tree1 = ParentedTree.convert(tree)
#tree.draw()
    m=0
    for t in tree1.subtrees():
        if t.label()=='SBAR':
            m=m+1   


    if (n+but)>0:
        #tokenized_sent=nltk.word_tokenize(sent10)
        #pos_tagged=nltk.pos_tag(tokenized_sent)
        sent1=sentence   
        sent=" ".join(tokenize(sent1))
        #print(sent)
        simplified=simplify(sent)
        for i in simplified:
            i=list(i)
            if ord(i[0])>=97 and ord(i[0])<=122:
                i[0]=chr(ord(i[0])-32)
            while i.count(",")>0:
                #i.pop(i.index(","))
                del(i[i.index(",")])
            if (".") not in(i):
                print("Simple sentence: "+"".join(i)+".")
            else:
                print("Simple sentence: "+"".join(i))
        n=0
        but=0
            #print("."),

    elif n==0 and m>0 and len(re.findall(r",",sentence))==0 and len(re.findall(r"While",sentence))==0:
        try:
            sent=sentence
            #print(sent)
            #print("Hello")
            tokenized_sent = tokenize(sent)
            pos_tagged = nltk.pos_tag(tokenized_sent)
            parse_trees=parser.tagged_parse(pos_tagged)
            sent_list=[s for s in sent.split()]
            tree=next(parse_trees)[0]
            #tree.draw()
            t=AnyNode(id='ROOT')
            make_tree_sbar(tree,t,sent_list)
            sbar=t
            vp_sbar=t
            vp=t
            np=t
            vbz='asvf'
            find_sbar(t)
            find_vp_in_sbar(sbar)
            f=True
            find_vp(t)
            f=True
            find_np(t)
            f=True
            find_vbz(t)
            simple_sentences=[]
            simple_sentences.append([])
            make_sent(np)
            make_sent(vp)
            simple_sentences.append([])
            make_sent(np)
            if vbz!='asvf':
                simple_sentences[-1].append(vbz)
            make_sent(vp_sbar)
            for i in simple_sentences:
                i=list(i)
            
   #             if ord(i[0])>=97 and ord(i[0])<=122:
    #                i[0]=chr(ord(i[0])-32)

                while i.count(",")>0:
                    i.pop(i.index(","))
                if (".") not in(i):
                    print("Simple sentence: "+" ".join(i)+".")
                else:
                    print("Simple sentence: "+" ".join(i))
            #print("."),
        except:
            continue
    elif m>0 and (len(re.findall(r",",sentence))>0 or len(re.findall(r"While",sentence))>0):
        try:
            #sent=re.sub(r",","",sentence)
            #print("Hello")
            tokenized_sent = tokenize(sentence)
            simple_sentences=SBAR.simplify(" ".join(tokenized_sent))
            for i in simple_sentences:
                #i=list(i)
            
       #             if ord(i[0])>=97 and ord(i[0])<=122:
    #                i[0]=chr(ord(i[0])-32)
    
                #while i.count(",")>0:
                  #  i.pop(i.index(","))
                if (".") not in(i):
                    print("Simple sentence: "+i)
                else:
                    print("Simple sentence: "+i)
            #print("."),
        except:
            continue

