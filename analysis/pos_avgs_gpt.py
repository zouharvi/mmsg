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
args.add_argument("--model", "-m", default="gpt2_base")
args = args.parse_args()

data = collate_classes(load_logs_machine(model=args.model))

ORDER = ['no_image', 'labels_text']
ORDER_COLUMN = ["Noun", "Verb", "Determiner", "Other"]


def flatten_second(data):
    return {
        config: [x for sent in data[config] for x in sent]
        for config in ORDER
    }


def confidence(vals):
    return st.t.interval(
        confidence=0.95,
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


fig = plt.figure(figsize=(5, 2.6))

data_pos_acc = defaultdict(lambda: defaultdict(list))
data_pos_cnf = defaultdict(lambda: defaultdict(list))
for config, config_data in data.items():
    for sent, ratings in zip(config_data["sent"], config_data["ratings"]):
        poss = nltk.pos_tag(sent.split())
        poss = [classify_pos(pos) for pos in poss]
        for pos,word in zip(poss, ratings):
            data_pos_acc[config][pos].append(word[1][1])
            data_pos_cnf[config][pos].append(word[0][1])

ax1 = plt.gca()
ax2 = ax1.twinx()

for pos_i, pos in enumerate(ORDER_COLUMN):
    # confidence
    ax1.bar(
        [x + pos_i / 5 - 0.3 for x in range(len(ORDER))],
        [np.average(data_pos_cnf[config][pos]) for config in ORDER],
        width=0.2, edgecolor="black",
        label=pos
    )
    cis = [
        np.abs(np.array(confidence(
            data_pos_cnf[config][pos])) - np.average(data_pos_cnf[config][pos]))
        for config in ORDER
    ]
    ax1.errorbar(
        x=[x + pos_i / 5 - 0.3 for x in range(len(ORDER))],
        y=[np.average(data_pos_cnf[config][pos]) for config in ORDER],
        yerr=np.array(cis).T,
        linewidth=0, elinewidth=1.5,
        color="black", capsize=3
    )

    # accuracy
    ax2.bar(
        [x + pos_i / 5 - 0.3 + 2 for x in range(len(ORDER))],
        [np.average(data_pos_acc[config][pos]) for config in ORDER],
        width=0.2, edgecolor="black",
        label=pos
    )
    cis = [
        np.abs(np.array(confidence(
            data_pos_acc[config][pos])) - np.average(data_pos_acc[config][pos]))
        for config in ORDER
    ]
    ax2.errorbar(
        x=[x + pos_i / 5 - 0.3 + 2 for x in range(len(ORDER))],
        y=[np.average(data_pos_acc[config][pos]) for config in ORDER],
        yerr=np.array(cis).T,
        linewidth=0, elinewidth=1.5,
        color="black", capsize=3
    )

ax1.vlines(
    x=1.5, ymin=0, ymax=0.6,
    linestyle=":", color="black"
)


XTICK_LABELS = [
    'No image', 'Labels text',
    'No image', 'Labels text',
]

plt.xticks(
    list(range(len(XTICK_LABELS))),
    [x.replace("_", " ") for x in XTICK_LABELS],
)

ax1.set_ylabel("Confidence")
ax2.set_ylabel("Accuracy")
ax1.set_ylim(
    0, 
    max([max([np.average(data_pos_cnf[config][pos]) for config in ORDER]) for pos in ORDER_COLUMN])+0.1
)
ax2.set_ylim(
    0, 
    max([max([np.average(data_pos_acc[config][pos]) for config in ORDER]) for pos in ORDER_COLUMN])+0.1
)

plt.text(0.5, -0.07, "Confidence", ha="center")
plt.text(2.5, -0.07, "Accuracy", ha="center")

plt.tight_layout(pad=0.01, rect=(0, 0, 1, 0.88))
plt.legend(
    ncol=4, bbox_to_anchor=(-0.05, 1.21),
    loc="upper left",
)

plt.savefig(os.environ['HOME'] + f"/Downloads/pos_avgs_{args.model}.pdf")
plt.show()
