from flask import g

import pymysql.cursors

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pymysql.connect(
            host="localhost",
            # host="serveurmysql",
            user="light@localhost",
            password="1234",
            database="TPNote",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return db
