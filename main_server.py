#!/usr/bin/env python3

import datetime, pytz, model, os, json, mturk
from housepy import config, log, server, util, process

process.secure_pid(os.path.join(os.path.dirname(__file__), "run"))

class Home(server.Handler):
    
    def get(self, page=None):
        if not len(page):
            return self.text("OK")    
        return self.not_found()

    def post(self, nop=None):
        log.info("Home.post")
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            hit_id = mturk.create_hit("https://s3.amazonaws.com/%s/%s.wav" % (config['s3']['bucket'], data['t']))
            model.add_clip(data['t'], hit_id)
        except Exception as e:
            return self.error(e)
        return self.text("OK")


handlers = [
    (r"/?([^/]*)", Home),
]    

server.start(handlers)