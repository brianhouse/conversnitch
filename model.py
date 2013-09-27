#!/usr/bin/env python3

import sqlite3, json, time, sys, os
from housepy import config, log, util

connection = sqlite3.connect(os.path.abspath(os.path.join(os.path.dirname(__file__), "data.db")))
connection.row_factory = sqlite3.Row
db = connection.cursor()

def init():
    try:
        db.execute("CREATE TABLE IF NOT EXISTS clips (t INTEGER, hit_id TEXT, posted INTEGER)")
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS clips_t ON clips(t)")
    except Exception as e:
        log.error(log.exc(e))
        return
    connection.commit()
init()

def add_clip(t, hit_id):
    try:
        db.execute("INSERT INTO clips (t, hit_id, posted) VALUES (?, ?, 0)", (t, hit_id))
    except Exception as e:
        log.error(log.exc(e))
        return
    log.info("Added clip %s %s" % (t, hit_id))
    connection.commit()

def get_recent():
    t = util.timestamp()
    db.execute("SELECT * FROM clips WHERE t>=? AND posted=0", (t - config['lag'],))
    # db.execute("SELECT * FROM clips WHERE posted=0")
    clips = [dict(clip) for clip in db.fetchall()]
    return clips

def mark_clip(t):
    log.info("Marking clip %s" % t)
    try:
        db.execute("UPDATE clips SET posted=1 WHERE t=?", (t,))
    except Exception as e:
        log.error(log.exc(e))
        return
    connection.commit()
