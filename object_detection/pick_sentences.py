#!/usr/bin/env python3

import json
import pickle
import os
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

data_control = []
lengths = Counter()


buckets_to_fulfill = defaultdict(lambda: 0) | {
    8: 4,
    9: 4,
    10: 4,
    11: 4,
    12: 4,
    13: 4,
    14: 4,
    15: 4,
}
used_imgs = set()
ANN_BAN = {407404, 22951}
buckets = []

with open("captions_val2017.json", "r") as f:
    data_coco = json.load(f)

for img in data_coco["images"]:
    # this is an inefficient but quick way to match annotations
    # ann["caption"] and ann["id"]
    captions = [{
            "url": img["coco_url"],
            "ann_id": ann["id"],
            "img_id": ann["image_id"],
            "caption": ann["caption"],
            "length": len(ann["caption"].split()),
        }
        for ann in data_coco["annotations"]
        if img["id"] == ann["image_id"]
    ]

    lengths.update([ann["length"] for ann in captions])

    for ann in captions:
        if (buckets_to_fulfill[ann["length"]] > 0) and (ann["img_id"] not in used_imgs) and (ann["ann_id"] not in ANN_BAN):
            used_imgs.add(ann["img_id"])
            buckets.append(ann)
            buckets_to_fulfill[ann["length"]] -= 1

print(lengths)
# plt.scatter(lengths.keys(), lengths.values())
# plt.show()

with open("sents_length.json", "w") as f:
    json.dump(buckets, f, indent=4)