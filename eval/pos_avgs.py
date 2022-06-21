#!/usr/bin/env python3

from utils import *
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import fig_utils
import os
import nltk
from argparse import ArgumentParser

args = ArgumentParser()
args.add_argument("-se", "--self-eval", action="store_true")
args = args.parse_args()

data = collate_classes(load_logs())

ORDER = ['no_image', 'original', 'labels_all', 'labels_crop', 'labels_text']
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


fig = plt.figure(figsize=(5, 2.5))
ax1 = fig.gca()
# plt.rcParams['hatch.linewidth'] = 0.5


data_pos = defaultdict(lambda: defaultdict(list))
for config, config_data in data.items():
    for sent, ratings in zip(config_data["sent"], config_data["ratings"]):
        poss = nltk.pos_tag(sent.split())
        poss = [classify_pos(pos) for pos in poss]
        for pos,word in zip(poss, ratings):
            if args.self_eval:
                data_pos[config][pos].append(word[1][1])
            else:
                data_pos[config][pos].append(word[0][1])

for pos_i, pos in enumerate(ORDER_COLUMN):
    plt.bar(
        [x + pos_i / 5 - 0.3 for x in range(len(ORDER))],
        [np.average(data_pos[config][pos]) for config in ORDER],
        width=0.2, edgecolor="black",
        label=pos
    )
    cis = [
        np.abs(np.array(confidence(
            data_pos[config][pos])) - np.average(data_pos[config][pos]))
        for config in ORDER
    ]
    plt.errorbar(
        x=[x + pos_i / 5 - 0.3 for x in range(len(ORDER))],
        y=[np.average(data_pos[config][pos]) for config in ORDER],
        yerr=np.array(cis).T,
        linewidth=0, elinewidth=1.5,
        color="black", capsize=3
    )


XTICK_LABELS = [
    'No_image', '\nOriginal',
    'Labels_all', '\nLabels_crop', 'Labels_text'
]

plt.xticks(
    list(range(len(XTICK_LABELS))),
    [x.replace("_", " ") for x in XTICK_LABELS],
    linespacing=0.2,
)

if args.self_eval:
    ax1.set_ylabel("Self-evaluation")
else:
    ax1.set_ylabel("Confidence")

plt.tight_layout(pad=0.01, rect=(0, 0, 1, 0.88))
plt.legend(
    ncol=4, bbox_to_anchor=(0.00, 1.19),
    loc="upper left",
)

if args.self_eval:
    plt.savefig(os.environ['HOME'] + "/Downloads/pos_avgs_eval.pdf")
else:
    plt.savefig(os.environ['HOME'] + "/Downloads/pos_avgs_conf.pdf")

plt.show()
