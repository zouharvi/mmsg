#!/usr/bin/env python3

import torch
import pandas as pd
import json
import pickle
from PIL import Image, ImageDraw, ImageFont
import os
from copy import deepcopy

# labels
# model.names

data_control = []

with open("captions_val2017.json", "r") as f:
    data_coco = json.load(f)

for img in data_coco["images"][:32]:
    # this is an inefficient but quick way to match annotations
    data_control.append({
        "url": img["coco_url"],
        "id": img["id"],
        "captions": [ann["caption"] for ann in data_coco["annotations"] if img["id"] == ann["image_id"]]
    })

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
results = model([img["url"] for img in data_control][:32])
data_detection = results.pandas().xyxy
results = results.tolist()

os.makedirs("img_data", exist_ok=True)
font = ImageFont.truetype('FreeMono.ttf', 20)

for i, (img, result) in enumerate(zip(data_control, results)):
    str_id = img["url"].split("/")[-1]
    img_dir = "img_data/" + str_id.rstrip(".jpg") + "/"
    os.makedirs(img_dir, exist_ok=True)

    img_0 = Image.fromarray(result.imgs[0])
    # TODO: are all jpegs?
    img_0.save(img_dir + "original.jpg")

    result_la = deepcopy(result)
    result_la.display(labels=True, crop=False, save=False, render=True)
    result_la = Image.fromarray(result_la.imgs[0])
    result_la.save(img_dir + "labels_all.jpg")

    result_ca = deepcopy(result)
    result_ca.display(labels=False, crop=False, save=False, render=True)
    result_ca = Image.fromarray(result_ca.imgs[0])
    result_ca.save(img_dir + "clear_all.jpg")

    result_lc = deepcopy(result)
    result_lc = result_lc.display(
        labels=True, crop=True, save=False, render=True
    )
    # the x["im"] variable is broken (channel missing) so we crop manually

    # dict_keys(['box', 'conf', 'cls', 'label', 'im'])
    for i, crop in enumerate(result_lc):
        tmp = img_0.copy()
        tmp = tmp.crop((
            int(crop["box"][0]),
            int(crop["box"][1]) - 20,
            int(crop["box"][2]),
            int(crop["box"][3]),
        ))

        min_width = font.getsize(crop["label"])[0]+5
        scale = min_width/float(crop["box"][2]-crop["box"][0])

        tmp = tmp.resize((
            int(tmp.width * scale),
            int((tmp.height-20) * scale + 20),
        ))
        tmp.save(img_dir + f"clear_crop_{i}.jpg")

        drawer = ImageDraw.Draw(tmp)
        drawer.rectangle(
            ((0, 0),
            (tmp.width, 20)),
            fill="black"
        )
        drawer.text((0,0), crop["label"], fill="white", font=font)
        tmp.save(img_dir + f"labels_crop_{i}.jpg")

    with open(img_dir+"meta.json", "w") as f:
        f.write(json.dumps({
            "labels": [x["label"] for x in result_lc],
            "caption": img["captions"]
        }))