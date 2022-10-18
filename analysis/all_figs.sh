#!/usr/bin/bash

# runs all scripts silently (without showing the figures)
DISPLAY= ./analysis/basic_avgs.py
DISPLAY= ./analysis/grade_conf.py
DISPLAY= ./analysis/pos_avgs.py
DISPLAY= ./analysis/pos_avgs.py -se
DISPLAY= ./analysis/sent_len.py