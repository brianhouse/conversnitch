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
        struct = mturk.retrieve_result(clip['hit_id'])   
        if struct is None:
            continue
        model.mark_clip(clip['t'])                        
        if 'nospeech' in struct and struct['nospeech'] == 'on':
            log.info("--> no speech in clip")
            continue
        try:
            for label in ('line_1', 'line_2', 'line_3'):
                if label in struct and len(struct[label]):
                    message = '"%s"' % struct[label]
                    ts.queue.put(message)
        except Exception as e:
            log.error(log.exc(e))
            continue        
    time.sleep(30)

