import csv
import sqlite3
from sqlite3 import Error

class YouTubeSQLite:

    def __init__(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
            self.c = self.conn.cursor()
            print(sqlite3.version)
        except Error as e:
            print(e)

    def create(self):
        try:
            self.c.execute("""CREATE TABLE youtube_entries
                     (title, channel_title, category_id, tags, views, likes, dislikes, comment_total)""")
        except Error as e:
            print(e)

    def insert(self, data):
        self.c.execute("""INSERT INTO youtube_entries 
                (title, channel_title, category_id, tags, views, likes, dislikes, comment_total)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                       (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
        self.conn.commit()

    def close(self):
        self.c.close()
        self.conn.close()



def __init__():
    db = YouTubeSQLite("youtubelite.sqlite")
    db.create()
    with open("youtube_subset.csv", "r", encoding="utf8") as f:
        reader = csv.reader(f, delimiter=",")
        accum = 1
        for line in reader:
            print(accum)
            accum += 1
            db.insert(line)
    print("done")
    db.close()



__init__()