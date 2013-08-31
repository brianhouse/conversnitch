#!/usr/bin/env python3

import sqlite3, json, time, sys, os, geojson
from housepy import config, log

connection = sqlite3.connect("data.db")
connection.row_factory = sqlite3.Row
db = connection.cursor()

def init():
    try:
        db.execute("CREATE TABLE IF NOT EXISTS clips (t INTEGER)")
        db.execute("CREATE INDEX IF NOT EXISTS clips_t ON clips(t)")
    except Exception as e:
        log.error(log.exc(e))
        return
    connection.commit()
init()

