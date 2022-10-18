#!/usr/bin/env python3

from utils import *
import numpy as np
import scipy.stats as st
import nltk 
import matplotlib.pyplot as plt

def cloze_prediction_pos(sent):
    sub = ((sentence['uid']).split("/")[1]).replace(".jsonl","")
    # print(sentence['sent'])
    sent = sentence['sent'].split()
    pos = nltk.pos_tag(sent)
    # print(pos)
    ratings = sentence['ratings']
    count_pos = {}
    easiness_pos = {}
    ez_cloze = {}
    for w_id in range(len(sent)):
        word = sent[w_id]
        rating_accuracy = ratings[w_id][0][1]
        pos_id = pos[w_id][1]
        
        if pos_id=="NN" or pos_id=="NNP" or pos_id=="NNS":
            pos_id = "Noun"
        elif pos_id=="VB" or pos_id=="VBD" or pos_id=="VBG" or pos_id=="VBN" or pos_id=="VBP" or pos_id=="VBZ":
            pos_id = "Verb"
        elif pos_id=="DT":
            pos_id = "Determiner"
        else:
            pos_id = "Others"
            
        if not pos_id in count_pos:
            count_pos[pos_id] = 1
        else:
            count_pos[pos_id] += 1

        if not pos_id in easiness_pos:
            easiness_pos[pos_id] = rating_accuracy
        else:
            easiness_pos[pos_id] += rating_accuracy
    
    for key in count_pos:
        cnt = float(count_pos[key])*5
        conf = float(easiness_pos[key])
        prob = conf/cnt
        ez_cloze[key]=np.around(abs(prob),3)
    
    return ez_cloze

def cloze_easiness_pos(sent):
    sub = ((sentence['uid']).split("/")[1]).replace(".jsonl","")
    # print(sentence['sent'])
    sent = sentence['sent'].split()
    pos = nltk.pos_tag(sent)
    # print(pos)
    ratings = sentence['ratings']
    count_pos = {}
    easiness_pos = {}
    ez_cloze = {}
    for w_id in range(len(sent)):
        word = sent[w_id]
        rating_accuracy = ratings[w_id][1][1]
        pos_id = pos[w_id][1]
        
        if pos_id=="NN" or pos_id=="NNP" or pos_id=="NNS":
            pos_id = "Noun"
        elif pos_id=="VB" or pos_id=="VBD" or pos_id=="VBG" or pos_id=="VBN" or pos_id=="VBP" or pos_id=="VBZ":
            pos_id = "Verb"
        elif pos_id=="DT":
            pos_id = "Determiner"
        else:
            pos_id = "Others"
            
        if not pos_id in count_pos:
            count_pos[pos_id] = 1
        else:
            count_pos[pos_id] += 1

        if not pos_id in easiness_pos:
            easiness_pos[pos_id] = rating_accuracy
        else:
            easiness_pos[pos_id] += rating_accuracy
    
    for key in count_pos:
        cnt = float(count_pos[key])*5
        conf = float(easiness_pos[key])
        prob = conf/cnt
        ez_cloze[key]=np.around(abs(prob),3)
    
    return ez_cloze

# POS_cloze={}

POS_prob_original = {}
POS_prob_labelscrop = {}
POS_prob_labelstext = {}
POS_prob_noimage = {}
POS_prob_labelsall = {}

data = load_logs()

# CLOZE EASINESS
for sentence in data:
    config = sentence['config']
    if config=="original":
        POS_prob = POS_prob_original
    elif config=="labels_crop":
        POS_prob = POS_prob_labelscrop
    elif config=="labels_text":
        POS_prob = POS_prob_labelstext
    elif config=="no_image":
        POS_prob = POS_prob_noimage
    elif config=="labels_all":
        POS_prob = POS_prob_labelsall    

    pos_cloze_easiness = cloze_easiness_pos(sentence)    
    for key in pos_cloze_easiness:
        if not key in POS_prob:
            POS_prob[key] = list()
        POS_prob[key].extend([pos_cloze_easiness[key]])

POS_cloze = {'original':POS_prob_original,
    'labels_crop':POS_prob_labelscrop,'labels_text':POS_prob_labelstext,
    'no_image':POS_prob_noimage,'labels_all':POS_prob_labelsall}

Noun = []
Verb = []
Determiner = []
Others = []

for key in POS_cloze:
    # print(key)
    dic = POS_cloze[key]
    noun = 0
    verb = 0
    others = 0
    determiner = 0
    for key in dic:
        if key=="Others":
            others = np.around(np.mean(dic[key]),3)
        if key=="Verb":
            verb = np.around(np.mean(dic[key]),3)
        if key=="Noun":
            noun = np.around(np.mean(dic[key]),3)
        if key=="Determiner":
            determiner = np.around(np.mean(dic[key]),3)
    Noun.append(noun)
    Verb.append(verb)
    Others.append(others)
    Determiner.append(determiner)

data = [Noun,Verb,Determiner,Others]
fig, ax = plt.subplots(1,1)
X = np.arange(5)
noun_stderr = np.std(data[0], ddof=1) / np.sqrt(len(data[0]))
ax.bar(X + 0.00, data[0], yerr= noun_stderr, capsize=4, color = 'royalblue', width = 0.15, label='Noun',)
verb_stderr = np.std(data[1], ddof=1) / np.sqrt(len(data[1]))
ax.bar(X + 0.15, data[1],  yerr= verb_stderr, capsize=4,color = 'lightcoral', width = 0.15, label='Verb')
detr_stderr = np.std(data[2], ddof=1) / np.sqrt(len(data[2]))
ax.bar(X + 0.30, data[2],  yerr= detr_stderr, capsize=4, edgecolor = 'royalblue', width = 0.15, label='Determiner',fill=False,hatch='-')
other_stderr = np.std(data[3], ddof=1) / np.sqrt(len(data[3]))
ax.bar(X + 0.45, data[3],  yerr= other_stderr, capsize=4,edgecolor = 'lightcoral', width = 0.15, label='Others',fill=False,hatch='*')

ax.set_ylabel('Prediction Accuracy')
ax.set_xlabel('Configurations')
x = np.arange(5)
width = 0.15
ax.set_xticks(x)
ax.set_xticklabels(['original','labels_crop','labels_text','no_image','labels_all'])
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=4, fancybox=True, shadow=True)
plt.savefig("Cloze_Easiness")



# CLOZE PREDICTION POS
for sentence in data:
    config = sentence['config']
    if config=="original":
        POS_prob = POS_prob_original
    elif config=="labels_crop":
        POS_prob = POS_prob_labelscrop
    elif config=="labels_text":
        POS_prob = POS_prob_labelstext
    elif config=="no_image":
        POS_prob = POS_prob_noimage
    elif config=="labels_all":
        POS_prob = POS_prob_labelsall    

    pos_cloze_easiness = cloze_prediction_pos(sentence)    
    for key in pos_cloze_easiness:
        if not key in POS_prob:
            POS_prob[key] = list()
        POS_prob[key].extend([pos_cloze_easiness[key]])

POS_cloze = {'original':POS_prob_original,
    'labels_crop':POS_prob_labelscrop,'labels_text':POS_prob_labelstext,
    'no_image':POS_prob_noimage,'labels_all':POS_prob_labelsall}

# POS_final = {}

# h = 'model\tNoun\tVerb\tOthers\n'
Noun = []
Verb = []
Determiner = []
Others = []

for key in POS_cloze:
    # print(key)
    dic = POS_cloze[key]
    noun = 0
    verb = 0
    others = 0
    determiner = 0
    for key in dic:
        if key=="Others":
            others = np.around(np.mean(dic[key]),3)
        if key=="Verb":
            verb = np.around(np.mean(dic[key]),3)
        if key=="Noun":
            noun = np.around(np.mean(dic[key]),3)
        if key=="Determiner":
            determiner = np.around(np.mean(dic[key]),3)
    Noun.append(noun)
    Verb.append(verb)
    Others.append(others)
    Determiner.append(determiner)
    # print(noun,verb,others,determiner)

data = [Noun,Verb,Determiner,Others]
fig, ax = plt.subplots(1,1)
X = np.arange(5)
noun_stderr = np.std(data[0], ddof=1) / np.sqrt(len(data[0]))
ax.bar(X + 0.00, data[0], yerr= noun_stderr, capsize=4, color = 'royalblue', width = 0.15, label='Noun',)
verb_stderr = np.std(data[1], ddof=1) / np.sqrt(len(data[1]))
ax.bar(X + 0.15, data[1],  yerr= verb_stderr, capsize=4,color = 'lightcoral', width = 0.15, label='Verb')
detr_stderr = np.std(data[2], ddof=1) / np.sqrt(len(data[2]))
ax.bar(X + 0.30, data[2],  yerr= detr_stderr, capsize=4, edgecolor = 'royalblue', width = 0.15, label='Determiner',fill=False,hatch='-')
other_stderr = np.std(data[3], ddof=1) / np.sqrt(len(data[3]))
ax.bar(X + 0.45, data[3],  yerr= other_stderr, capsize=4,edgecolor = 'lightcoral', width = 0.15, label='Others',fill=False,hatch='*')

ax.set_ylabel('Prediction confidence')
ax.set_xlabel('Configurations')
x = np.arange(5)
width = 0.15
ax.set_xticks(x)
ax.set_xticklabels(['original','labels_crop','labels_text','no_image','labels_all'])
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=4, fancybox=True, shadow=True)
plt.savefig("Cloze_Prediction")
