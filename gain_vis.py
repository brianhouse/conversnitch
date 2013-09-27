#!/usr/bin/env python3

import time, json, threading, subprocess, queue, platform, os, sys
import numpy as np
from housepy import log, config, strings, net, s3, util, process, drawing
from scipy.io import wavfile

DURATION = 10
AUDIO_TMP = os.path.abspath(os.path.join(os.path.dirname(__file__), "audio_tmp"))

t = sys.argv[1]

filename = "%s/%s.wav" % (AUDIO_TMP, t)
sample_rate, signal = wavfile.read(filename)
log.debug("samples %s" % len(signal))
log.debug("sample_rate %s" % sample_rate)
duration = float(len(signal)) / sample_rate
log.debug("duration %ss" % strings.format_time(duration))
signal = (np.array(signal).astype('float') / (2**16 * 0.5))   # assuming 16-bit PCM, -1 - 1
signal = abs(signal)    # magnitude

ctx = drawing.Context()
ctx.plot(signal)
ctx.line(0, config['noise_threshold'], 1, config['noise_threshold'], stroke=(255, 0, 0))
ctx.output("screenshots")

log.debug("noise threshold is %s" % config['noise_threshold'])
log.debug("found magnitude")
content_samples = 0
for sample in signal:
    if sample > config['noise_threshold']:
        content_samples += 1
total_content_time = float(content_samples) / sample_rate
log.info("total_content_time %s" % total_content_time)

