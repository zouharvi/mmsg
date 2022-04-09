#!/usr/bin/env python3

import json
import pickle
import os
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from argparse import ArgumentParser

args = ArgumentParser()
args.add_argument("-d", "--dev", action="store_true")
args = args.parse_args()

data_control = []
lengths = Counter()

buckets_to_fulfill = defaultdict(lambda: 0) | {
    8: 2,
    9: 2,
    10: 2,
    11: 2,
    12: 2,
    13: 2,
    14: 2,
    15: 2,
}
used_imgs = set()
ANN_BAN = {407404, 22951}
buckets = []

with open("captions_val2017.json", "r") as f:
    data_coco = json.load(f)

print("Total count:", len(data_coco["images"]))

for img_i, img in enumerate(data_coco["images"][(50 if args.dev else 0):]):
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
        if img["id"] == ann["image_id"] and not ann["caption"].isupper() and "  " not in ann["caption"]
    ]

    lengths.update([ann["length"] for ann in captions])

    for ann in captions:
        if (buckets_to_fulfill[ann["length"]] > 0) and (ann["img_id"] not in used_imgs) and (ann["ann_id"] not in ANN_BAN):
            used_imgs.add(ann["img_id"])
            buckets.append(ann)
            buckets_to_fulfill[ann["length"]] -= 1
            print("img_i:", img_i)
            break
    
    if sum(buckets_to_fulfill.values()) == 0:
        break


print(lengths)
# plt.scatter(lengths.keys(), lengths.values())
# plt.show()

with open(f"baked_queues/sents_length{'_dev' if args.dev else ''}.json", "w") as f:
    json.dump(buckets, f, indent=4)