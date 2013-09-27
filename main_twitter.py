#!/usr/bin/env python3

import model, mturk, tweet_sender, time, os
from housepy import config, log, process, util

ts = tweet_sender.TweetSender()

process.secure_pid(os.path.abspath(os.path.join(os.path.dirname(__file__), "run")))

while True:
    log.info("//////////")
    clips = model.get_recent()
    log.info("%s recent clips" % len(clips))
    for clip in clips:
        log.info("Checking %s %s %s" % (clip['t'], clip['hit_id'], util.datestring(clip['t'])))
        text = mturk.retrieve_result(clip['hit_id'])        
        if text is not None:
            model.mark_clip(clip['t'])
            ts.queue.put(text)
    time.sleep(10)