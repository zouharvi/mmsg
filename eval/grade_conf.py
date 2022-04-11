#!/usr/bin/env python3

from utils import *
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import fig_utils
import os
from collections import Counter

data = collate_classes(load_logs())

fig, ax = plt.subplots(ncols=5, figsize=(11, 2.6))

def config_tilemap(data, ax_i, name=""):
    counts = Counter({(x0, x1):0 for x0 in range(5) for x1 in range(5)})
    for sent in data:
        counts.update([(word[0][1], word[1][1]) for word in sent])
    img = np.zeros((5, 5), dtype=np.int)
    for (x0, x1), v in counts.items():
        if x1 == -1:
            continue
        img[x0, x1] = v

    img_render = ax[ax_i].imshow(
        np.sqrt(img), origin="lower", cmap="viridis",
        norm=Normalize(vmin=0, vmax=8, clip=True)
    )

    for (x0, x1), v in counts.items():
        if x1 != -1:
            ax[ax_i].text(
                x1, x0, v,
                ha="center", va="center",
                color="black" if v > 3 else "lightgray"
            )

    ax[ax_i].set_xlabel(r"$\bf{" + name.replace('_', '\,\,').capitalize() + "}$ (confidence)")
    if ax_i == 0:
        # cbar = ax[ax_i].figure.colorbar(img_render)
        ax[ax_i].set_ylabel("Self-evaluation")
    else:
        ax[ax_i].get_yaxis().set_visible(False)

    # ax[ax_i].set_title(name.replace("_", " ").capitalize())


config_tilemap(data["no_image"]["ratings"], ax_i=0, name="no_image")
config_tilemap(data["original"]["ratings"], ax_i=1, name="original")
config_tilemap(data["labels_all"]["ratings"], ax_i=2, name="labels_all")
config_tilemap(data["labels_crop"]["ratings"], ax_i=3, name="labels_crop")
config_tilemap(data["labels_text"]["ratings"], ax_i=4, name="labels_text")

plt.tight_layout(pad=0.1, rect=(0, 0, 1, 1.12))
plt.savefig(os.environ['HOME'] + "/Downloads/grade_conf.pdf")
plt.show()