#!/usr/bin/env python3

import sqlite3, json, time, sys, os
from housepy import config, log, util

def db_call(f):
    def wrapper(*args):
        connection = sqlite3.connect(os.path.abspath(os.path.join(os.path.dirname(__file__), "data.db")))
        connection.row_factory = sqlite3.Row
        db = connection.cursor()
        results = f(db, *args)
        connection.commit()
        connection.close()
        return results
    return wrapper

@db_call
def init(db):
    try:
        db.execute("CREATE TABLE IF NOT EXISTS clips (t INTEGER, hit_id TEXT, posted INTEGER)")
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS clips_t ON clips(t)")
    except Exception as e:
        log.error(log.exc(e))
        return
init()

@db_call
def add_clip(db, t, hit_id):
    try:
        db.execute("INSERT INTO clips (t, hit_id, posted) VALUES (?, ?, 0)", (t, hit_id))
    except Exception as e:
        log.error(log.exc(e))
        return
    log.info("Added clip %s %s" % (t, hit_id))

@db_call
def get_recent(db):
    t = util.timestamp()
    db.execute("SELECT * FROM clips WHERE t>=? AND posted=0", (t - config['lag'],))
    clips = [dict(clip) for clip in db.fetchall()]
    return clips

@db_call
def mark_clip(db, t):
    log.info("Marking clip %s" % t)
    try:
        db.execute("UPDATE clips SET posted=1 WHERE t=?", (t,))
    except Exception as e:
        log.error(log.exc(e))
        return
