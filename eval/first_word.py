#!/usr/bin/env python3

from utils import *
import numpy as np
import os
from collections import Counter
import nltk

data = collate_classes(load_logs())


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


def config_tilemap(data, name):
    print("="*10)
    print(name)
    counts_conf = Counter({x0:0 for x0 in range(5)})
    counts_eval = Counter({x0:0 for x0 in range(5)})
    counts_pos = Counter()
    vals_conf = []
    vals_eval = []
    for ratings, sent in zip(data["ratings"], data["sent"]):
        poss = nltk.pos_tag(sent.split())
        pos = classify_pos(poss[0])
        counts_pos.update([pos])
        # print(pos)
        counts_conf.update([ratings[0][0][1]])
        counts_eval.update([ratings[0][1][1]])
        vals_conf.append(ratings[0][0][1])
        vals_eval.append(ratings[0][1][1])
    
    print("Conf.:", [counts_conf[x0] for x0 in range(5)], np.average(vals_conf))
    print("Eval.:", [counts_eval[x0] for x0 in range(5)], np.average(vals_eval))
    print("POS:", counts_pos.items())


config_tilemap(data["no_image"], name="no_image")
config_tilemap(data["original"], name="original")
config_tilemap(data["labels_all"], name="labels_all")
config_tilemap(data["labels_crop"], name="labels_crop")
config_tilemap(data["labels_text"], name="labels_text")