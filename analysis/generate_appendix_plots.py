#!/usr/bin/env python3

from utils import *
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import fig_utils
import os
import nltk
from argparse import ArgumentParser
from scipy import stats
from scipy.stats import sem

args = ArgumentParser()
args.add_argument("-se", "--self-eval", action="store_true")
args = args.parse_args()



data_hum = collate_classes(load_logs())
data_machine = collate_classes(load_logs_machine(model="gpt2_base"))



ORDER = ['no_image', 'labels_text']

ORDER_COLUMN = ["Noun", "Verb", "Determiner", "Other"]


def flatten_second(data):
    return {
        config: [x for sent in data[config] for x in sent]
        for config in ORDER
    }


def confidence(vals):
    return st.t.interval(
        alpha=0.95,
        df=len(vals) - 1,
        loc=np.mean(vals),
        scale=st.sem(vals)
    )


def classify_pos(pos):
    pos = pos[1]
    if pos == "NN" or pos == "NNP" or pos == "NNS":
        return "Noun"
    elif pos == "VB" or pos == "VBD" or pos == "VBG" or pos == "VBN" or pos == "VBP" or pos == "VBZ":
        return "Verb"
    elif pos == "DT":
        return "Determiner"
    else:
        return "Other"


# fig = plt.figure(figsize=(5, 2.5))
# ax1 = fig.gca()
# # plt.rcParams['hatch.linewidth'] = 0.5

data_pos_conf_hum = defaultdict(lambda: defaultdict(list))
data_pos_conf_gpt = defaultdict(lambda: defaultdict(list))
data_pos_acc_hum  = defaultdict(lambda: defaultdict(list))
data_pos_acc_gpt  = defaultdict(lambda: defaultdict(list))

for config in ORDER:   

    for ac_config in ORDER:
        for config, config_data in data_hum.items():
            if ac_config==config:
                for sent, ratings, sent_id in zip(config_data["sent"], config_data["ratings"],config_data["id"]):
            
                    gpt_index = [i for i,x in enumerate(data_machine[config]["id"]) if x == sent_id][0]
                    gpt_ratings = data_machine[config]["ratings"][gpt_index]
            
                    poss = nltk.pos_tag(sent.split())
                    poss = [classify_pos(pos) for pos in poss]
                    for pos,word,word_gpt in zip(poss, ratings,gpt_ratings):
                        data_pos_acc_hum[config][pos].append(word[1][1])
                        data_pos_acc_gpt[config][pos].append(word_gpt[1][1])
                        data_pos_conf_hum[config][pos].append(word[0][1])
                        data_pos_conf_gpt[config][pos].append(word_gpt[0][1])



# for config in ORDER:   
#     conf = []
#     acc  = []
#     for pos_i, pos in enumerate(ORDER_COLUMN):
#         human_conf = data_pos_conf_hum[config][pos]
#         machine_conf = data_pos_conf_hum[config][pos]
#         PCC_Conf = np.corrcoef(human_conf,machine_conf)[0,1]
#         plt.plot()

#         human_acc = data_pos_acc_hum[config][pos]
#         machine_acc = data_pos_acc_hum[config][pos]
#         PCC_Acc = np.corrcoef(human_acc,machine_acc)[0,1]

        
        

for config in ORDER:
    conf =[]
    acc = []
    for pos_i, pos in enumerate(ORDER_COLUMN):
        human_conf = data_pos_conf_hum[config][pos]
        machine_conf = data_pos_conf_gpt[config][pos]
        PCC_Conf = np.corrcoef(human_conf,machine_conf)[0,1]
        conf.append(PCC_Conf)

        human_acc = data_pos_acc_hum[config][pos]
        machine_acc = data_pos_acc_gpt[config][pos]
        PCC_Acc = np.corrcoef(human_acc,machine_acc)[0,1]
        acc.append(PCC_Acc)

    plt.scatter(np.arange(len(ORDER_COLUMN)),conf,label="confidence"+"_"+config)
    plt.scatter(np.arange(len(ORDER_COLUMN)),acc,label="accurcacy"+"_"+config)

plt.xticks(np.arange(len(ORDER_COLUMN)), ORDER_COLUMN)
plt.title("Correlation between human and machine metrics for POS labels")
plt.xlabel("POS categories")
plt.ylabel("Pearson Correlation Coefficient")
plt.legend()
plt.savefig("corr.pdf")
plt.close()
plt.clf()

for config in ORDER:
    conf =[]
    acc = []
    if config=="labels_text":
        fill = 'full'
    else:
        fill = 'none'

    for pos_i, pos in enumerate(ORDER_COLUMN):
        if pos=="Noun":
            marker = "o"
        elif pos=="Verb":
            marker = "s"
        elif pos=="Determiner":
            marker = "^"
        elif pos=="Other":
            marker = "v"

        human_conf = data_pos_conf_hum[config][pos]
        machine_conf = data_pos_conf_gpt[config][pos]
        plt.scatter(np.average(human_conf),np.average(machine_conf),label="confidence"+"_"+pos,color='red',marker=marker)
    
        human_acc = data_pos_acc_hum[config][pos]
        machine_acc = data_pos_acc_gpt[config][pos]
        plt.scatter(np.average(human_acc),np.average(machine_acc),label="accurcacy"+"_"+pos,color='green',marker=marker)
        
    plt.xticks(np.arange(len(ORDER_COLUMN)))
    plt.title("Human vs Machine ratings for POS labels")
    plt.xlabel("Humans")
    plt.ylabel("GPT2")
    plt.legend(bbox_to_anchor =(1.05, 1),loc='best')
    plt.legend()
    name = "detail_"+config+".pdf"
    plt.savefig(name)
    plt.close()
    plt.clf()