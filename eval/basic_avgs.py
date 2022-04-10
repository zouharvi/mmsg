#!/usr/bin/env python3

from utils import *
import numpy as np
import scipy.stats as st

data = collate_classes(load_logs(["lusaka"]))

def flatten_second(data):
    return {
        config:[x for sent in lll for x in sent]
        for config,lll in data.items()
    }

def confidence(vals):
    ci = st.t.interval(
        alpha=0.95,
        df=len(vals)-1,
        loc=np.mean(vals),
        scale=st.sem(vals)
    )
    return f"{ci[0]:.2f}, {ci[1]:.2f}"

def avg_pprint(data, name=""):
    print("="*10 + " " + name +" " + "="*10)
    for config,vals in data.items():
        print(f"{config:<15}: {np.average(vals):.2f} ({confidence(vals)})")
    print()

# confidence
data_conf = flatten_second({
    config:[[x[0][1] for x in sent] for sent in lll["ratings"]]
    for config, lll in data.items()
})
data_conf_time = flatten_second({
    config:[[x[0][0] for x in sent] for sent in lll["ratings"]]
    for config, lll in data.items()
})
# self-eval
data_eval = flatten_second({
    config:[[x[1][1] for x in sent] for sent in lll["ratings"]]
    for config, lll in data.items()
})
data_eval_time = flatten_second({
    config:[[x[1][0] for x in sent] for sent in lll["ratings"]]
    for config, lll in data.items()
})

avg_pprint(data_conf, name="avg. confidence score")
avg_pprint(data_eval, name="avg. self-eval score")
avg_pprint(data_conf_time, name="avg. confidence time")
avg_pprint(data_eval_time, name="avg. self-eval time")