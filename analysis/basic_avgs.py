#!/usr/bin/env python3

from utils import *
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import fig_utils
import os

data = collate_classes(load_logs())

ORDER = ['no_image', 'original', 'labels_all', 'labels_crop', 'labels_text']


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


def avg_pprint(data, name=""):
    print("=" * 10 + " " + name + " " + "=" * 10)
    for config, vals in data.items():
        ci = confidence(vals)
        print(
            f"{config:<15}: {np.average(vals):.2f} ({ci[0]:.2f}, {ci[1]:.2f})"
        )
    print()


fig = plt.figure(figsize=(5, 2.8))
ax1 = fig.gca()
ax2 = ax1.twinx()
plt.rcParams['hatch.linewidth'] = 0.5


def avg_plotbar(data, name="", i=0, color="black", hatch="", ax=ax1):
    ax.bar(
        [x + i / 5 - 0.3 for x in range(len(data.keys()))],
        [np.average(x) for x in data.values()],
        width=0.2, edgecolor="black",
        label=name, color=color, hatch=hatch,
    )
    cis = [np.abs(np.array(confidence(x)) - np.average(x))
           for x in data.values()]
    print(cis)
    # print(cis[0])
    # ax.scatter(
    #     2*[x + i / 5 - 0.3 for x in range(len(data.keys()))],
    #     [x[0] for x in cis]+[x[1] for x in cis],
    #     color="black",
    #     zorder=10, s=10, marker="$-$"
    # )
    ax.errorbar(
        x=[x + i / 5 - 0.3 for x in range(len(data.keys()))],
        y=[np.average(x) for x in data.values()],
        yerr=np.array(cis).T,
        linewidth=0, elinewidth=1.5,
        color="black", capsize=3
    )


# confidence
data_conf = flatten_second({
    config: [[x[0][1] for x in sent] for sent in lll["ratings"]]
    for config, lll in data.items()
})
data_conf_time = flatten_second({
    config: [[x[0][0] for x in sent] for sent in lll["ratings"]]
    for config, lll in data.items()
})

# self-eval
data_eval = flatten_second({
    config: [
        [x[1][1] for x in sent if x[1][1] >= 0]
        for sent in lll["ratings"]
    ]
    for config, lll in data.items()
})
data_eval_time = flatten_second({
    config: [[x[1][0] for x in sent] for sent in lll["ratings"]]
    for config, lll in data.items()
})

# time medians
print(np.median([x for l in data_conf_time.values() for x in l]))
print(np.median([x for l in data_eval_time.values() for x in l]))

avg_pprint(data_conf, name="avg. confidence score")
avg_pprint(data_eval, name="avg. self-eval score")
avg_pprint(data_conf_time, name="avg. confidence time")
avg_pprint(data_eval_time, name="avg. self-eval time")

avg_plotbar(data_conf, name="Confidence score", i=0, color="cornflowerblue")
avg_plotbar(data_eval, name="Self-eval score", i=1, color="salmon")
avg_plotbar(
    data_conf_time, name="Confidence time",
    i=2, color="cornflowerblue", hatch="..", ax=ax2,
)
avg_plotbar(
    data_eval_time, name="Self-eval time",
    i=3, color="salmon", hatch="..", ax=ax2,
)

XTICK_LABELS = [
    'No_image', '\nOriginal',
    'Labels_all', '\nLabels_crop', 'Labels_text',
]

ax1.set_xticks(
    list(range(len(XTICK_LABELS))),
    [x.replace("_", " ") for x in XTICK_LABELS],
    linespacing=0.3,
)

ax1.set_ylabel("Rating")
ax2.set_ylabel("Time (s)")

h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()

plt.tight_layout(pad=0, rect=(0, 0, 1, 0.81))
plt.legend(
    h1 + h2, l1 + l2,
    ncol=2, bbox_to_anchor=(0.04, 1.3),
    loc="upper left",
)
plt.savefig(os.environ['HOME'] + "/Downloads/basic_avgs.pdf")
plt.show()
