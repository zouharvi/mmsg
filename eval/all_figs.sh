#!/usr/bin/bash

# runs all scripts silently (without showing the figures)
DISPLAY= ./basic_avgs.py
DISPLAY= ./grade_conf.py
DISPLAY= ./pos_avgs.py
DISPLAY= ./pos_avgs.py -se
DISPLAY= ./sent_len.py