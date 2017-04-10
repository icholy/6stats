#!/usr/bin/env python

import json
import pprint
import sqlite3
import ipdb
import dateutil.parser

def read_json(filename):
    with open(filename) as f:
        return json.load(f)

CREATE_QUERY = '''
    CREATE TABLE IF NOT EXISTS messages (
        date datetime,
        user text,
        text text
    )
'''

INSERT_QUERY = '''
    INSERT INTO messages VALUES (?, ?, ?)
'''

def main():

    with sqlite3.connect("messages.db") as conn:
        cur = conn.cursor()
        cur.execute(CREATE_QUERY)
        for m in read_json("the6.json"):
            date = dateutil.parser.parse(m["date"])
            params = (date, m["user"], m["text"])
            cur.execute(INSERT_QUERY, params)
        conn.commit()

if __name__ == "__main__":
    main()

