#!/usr/bin/env python3

from utils import *
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import fig_utils
import os
from collections import defaultdict

data = collate_classes(load_logs())

ORDER = ['no_image', 'original', 'labels_all', 'labels_crop', 'labels_text']

def flatten_second(data):
    return {
        config: [x for sent in data[config] for x in sent]
        for config in ORDER
    }

fig = plt.figure(figsize=(5, 4))
ax1 = fig.gca()
ax2 = ax1.twinx()

def sent_len(getter=lambda x: None, name="", linestyle="-", color="black", ax=ax1):
    counts = defaultdict(list)
    for subdata in data.values():
        for sent in subdata["ratings"]:
            for word_i, word in enumerate(sent):
                counts[word_i].append(getter(word))
    
    ax.plot(
        counts.keys(),
        [np.average(x) for x in counts.values()],
        label=name, color=color, linestyle=linestyle
    )
    
sent_len(getter=lambda x: x[0][1], name="Confidence score", color="cornflowerblue", linestyle="-", ax=ax1)
sent_len(getter=lambda x: x[1][1], name="Self-eval score", color="salmon", linestyle="-", ax=ax1)
sent_len(getter=lambda x: x[0][0], name="Confidence time", color="cornflowerblue", linestyle=":", ax=ax2)
sent_len(getter=lambda x: x[1][0], name="Self-eval time", color="salmon", linestyle=":", ax=ax2)

ax1.set_ylabel("Rating")
ax1.set_xlabel("Sentence length")
ax2.set_ylabel("Time (s)")

plt.tight_layout(pad=0, rect=(0, 0, 1, 0.85))

h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
plt.legend(
    h1 + h2, l1 + l2,
    ncol=2, bbox_to_anchor=(0.04, 1.2),
    loc="upper left",
)

plt.savefig(os.environ['HOME'] + "/Downloads/sent_len.pdf")
plt.show()