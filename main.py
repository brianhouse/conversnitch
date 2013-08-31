#!/usr/bin/env python3

import datetime, pytz, model, os, json
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
            log.debug(data)
        except Exception as e:
            return self.error(e)
        return self.text("OK")


handlers = [
    (r"/?([^/]*)", Home),
]    

server.start(handlers)
