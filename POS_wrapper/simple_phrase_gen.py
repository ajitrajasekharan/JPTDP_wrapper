#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#

from __future__ import print_function
import sys
import pdb
import math
import traceback

WORD_INDEX = 1
POS_INDEX = 2
ORD_INDEX = 3
DEP_INDEX = 4


full_tag_set = ['PRP$', 'VBG', 'VBD', 'NFP', '``', 'ROOT-POS', "''", 'VBP', 'VBN', 'JJ', 'WP', 'VBZ', 'DT', 'RP', '$', 'NN', 'FW', ',', '.', 'TO', 'PRP', 'RB', '-LRB-', ':', 'NNS', 'HYPH', 'VB', 'WRB', 'CC', 'LS', 'PDT', 'RBS', 'RBR', 'CD', 'AFX', 'EX', 'IN', 'WP$', 'MD', 'NNPS', '-RRB-', 'POS', 'JJS', 'JJR', 'SYM', 'UH', 'WDT', 'NNP']

push_tags = ['NFP', '``', 'ROOT-POS', "''", 'JJ','NN',  'FW', '.', ':', 'NNS', 'HYPH', 'PDT',  'AFX', 'EX','NNPS', 'POS', 'JJS', 'JJR',  'NNP','RB','VBG','IN']

pop_tags = ['PRP$', 'VBD', 'VBN', 'WP', 'VBZ', 'DT', 'RP', 'PRP',   'VB', 'WRB', 'CC', 'LS', 'PDT', 'RBS', 'RBR', 'CD', 'AFX', 'EX',  'WP$', 'MD',  '-RRB-', 'POS',   'UH', 'WDT','TO','VB','VBN',',','-LRB-','WP$','WRB','$','SYM']

trail_tags = ['VBG','IN']

punctuations_arr = ['>', '<', '=']


prepositions_arr = [
"about",
"below",
"excepting",
"off",
"toward",
"above",
"beneath",
"for",
"on",
"under",
"across",
"besides",
"from",
"onto",
"underneath",
"after",
"between",
"in",
"out",
"until",
"against",
"beyond",
"in front of",
"outside",
"up",
"along",
"but",
"inside",
"over",
"upon",
"among",
"by",
"in spite of",
"past",
"up to",
"around",
"concerning",
"instead of",
"regarding",
"with",
"at ",
"despite",
"into",
"since",
"within",
"because of",
"down",
"like",
"through",
"without",
"before",
"during",
"near",
"throughout",
"with regard to",
"behind",
"except",
"of",
"to",
"with respect to",
"about",
"below",
"excepting",
"off",
"toward",
"above",
"beneath",
"for",
"on",
"under",
"across",
"from",
"onto",
"underneath",
"after",
"between",
"in",
"out",
"until",
"against",
"beyond",
"in front of",
"outside",
"up",
"along",
"but",
"inside",
"over",
"upon",
"among",
"by",
"in spite of",
"past",
"up to",
"around",
"concerning",
"instead of",
"regarding",
"with",
"at ",
"despite",
"into",
"since",
"within",
"because of",
"down",
"like",
"through",
"without",
"before",
"during",
"near",
"throughout",
"with regard to",
"behind",
"except",
"of",
"to",
"with respect to"
]



def correct_dep_fields_if_error(fields):
    #pdb.set_trace()
    if (fields[POS_INDEX] == 'IN' and fields[WORD_INDEX] not in prepositions_arr):
        fields[POS_INDEX] = 'NN'
    elif ((fields[POS_INDEX] == 'CD' or fields[POS_INDEX] == 'NN') and fields[WORD_INDEX]  in punctuations_arr):
        fields[POS_INDEX] = 'SYM'



#push_tags = ['NFP', '``', 'ROOT-POS', "''", 'JJ',   '$','NN',  'FW', ',', '.', '-LRB-', ':', 'NNS', 'HYPH', 'VB', 'WRB',  'LS', 'PDT', 'RBS', 'RBR', 'CD', 'AFX', 'EX',  'WP$', 'MD', 'NNPS', '-RRB-', 'POS', 'JJS', 'JJR', 'SYM', 'UH', 'WDT', 'NNP','VBN','IN','TO']

#pop_tags = ['PRP$', 'VBG', 'VBD', 'VBN', 'WP', 'VBZ', 'DT', 'RP', 'PRP', 'RB',   'VB', 'WRB', 'CC', 'LS', 'PDT', 'RBS', 'RBR', 'CD', 'AFX', 'EX',  'WP$', 'MD',  '-RRB-', 'POS',   'UH', 'WDT']


#strict_pop_tags = {"ADP","DET", "CCONJ", "PRON","PART", "AUX", "SCONJ",  "X", "INTJ", "ROOT-POS","PUNCT" }
#strict_push_tags = { "ADV", "ADJ", "NOUN", "NUM",  "PROPN",  "SYM","VERB"}

pop_addl_tags = {"parataxis"}


#relaxed_pop_tags = {"PRON","AUX", "X", "INTJ", "ROOT-POS","PUNCT" }
#relaxed_push_tags = {"ADP","DET","CCONJ","PART","SCONJ","ADV", "ADJ", "NOUN", "NUM",  "PROPN",  "SYM","VERB"}

#push_tags = strict_push_tags
#pop_tags = strict_pop_tags



def find_trailing_stopwords(stk,tag_stk,stopwords_dict):
    i = len(stk) - 1
    while i >= 0 :
        if (stk[i] not in stopwords_dict and tag_stk[i] not in trail_tags):
            break
        i -= 1
    return i

def emit_stack(stk,tag_stack,stopwords_dict):
    #pdb.set_trace()
    end_index = find_trailing_stopwords(stk,tag_stack,stopwords_dict)
    #if (len(stk) > 0):
    #    print(stk)
    #stk[:] = []
    #return
    is_firstword_stopword=False
    for i in range(len(stk)):
        if (i == 0 and stk[i] in stopwords_dict):
            is_firstword_stopword = True
        if (i > 0):
            if (i > end_index):
                    print(' ',end='')
            else:
                if (is_firstword_stopword == True):
                    print(' ',end='')
                    if (stk[i]  not in stopwords_dict):
                            is_firstword_stopword = False
                else:
                    print("_",end='')
        print(stk[i].strip().rstrip('.'),end='')
    if (len(stk) > 0):
        print(' ',end='')
    stk[:] = []
    tag_stack[:] = []


def read_stopwords(stopwords_file):
    arr = []
    with open(stopwords_file) as fin:
        for line in fin:
            fields = line.split(' ')
            if (len(fields) >= 1):
                arr.append(fields[0])
    return arr

#This addresses a bunch of quirks in jPTDP output

def in_push_list(term,tag):
    if (tag in push_tags):
        if ((tag == '.' and term  != '.') or (tag == ':' and term != ':')):
            return False
        elif (term in punctuations_arr and (tag == "NN" or tag == "NNP")):
            return False
        else:
            return True
    else:
        return False



def gen_phrases(fname,stopwords_dict,ngram_limit,is_strict):
    #with open(fname,'r',buffering=20*(1024**2)) as fin:
    #pdb.set_trace()
    with open(fname,'r') as fin:
        stk = []
        tag_stack = []
        for line in fin:
            fields = line.split('\t')
            if (len(fields) >= 3):
                correct_dep_fields_if_error(fields)
                term = fields[WORD_INDEX]
                #print(term)
                #pdb.set_trace()
                #print ("***",fields[WORD_INDEX],fields[3])
                if (in_push_list(term,fields[POS_INDEX]) and  (is_strict == 0  or (fields[DEP_INDEX] not in pop_addl_tags and term not in stopwords_dict))):
                    #print("PUSH:",fields[1],len(stk))
                    stk.append(fields[WORD_INDEX])
                    tag_stack.append(fields[POS_INDEX])
                    if (len(stk) >= ngram_limit):
                        emit_stack(stk,tag_stack,stopwords_dict)
                #elif (fields[POS_INDEX] in pop_tags or fields[DEP_INDEX] in pop_addl_tags or term in stopwords_dict):
                else:
                    #pdb.set_trace()
                    emit_stack(stk,tag_stack,stopwords_dict)
                    #print("POP:",fields[POS_INDEX])
                    stk.append(fields[WORD_INDEX])
                    tag_stack.append(fields[POS_INDEX])
                    emit_stack(stk,tag_stack,stopwords_dict)
            else:
                if (len(stk) > 0):
                    emit_stack(stk,tag_stack,stopwords_dict)
                print("\n")
                #print("**************NEW LINE")



if __name__ == '__main__':
    try:
        arr = read_stopwords(sys.argv[2])


        gen_phrases(sys.argv[1],arr,int(sys.argv[3]),0)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
