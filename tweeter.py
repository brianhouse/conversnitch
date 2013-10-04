#!/usr/bin/env python3

import model, mturk, tweet_sender, time, os, sys
from housepy import config, log, process, util



message = sys.argv[1]
message = '"%s"' % message.strip('"')[:138]
print(message)

ts = tweet_sender.TweetSender()
ts.queue.put(message)

time.sleep(3)



