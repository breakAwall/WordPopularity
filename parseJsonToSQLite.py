import json
import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np
import time

class UrbanSQLite:

    def __init__(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
            self.c = self.conn.cursor()
            # print(sqlite3.version)
        except Error as e:
            print(e)

    def create(self):
        try:
            self.c.execute("""CREATE TABLE per_word
                     (word, thumbs_up, thumbs_down)""")
        except Error as e:
            print(e)

    def insert(self, data):
        self.c.execute("INSERT INTO per_word (word, thumbs_up, thumbs_down)VALUES (?, ?, ?)",
                       (data["lowercase_word"], data['thumbs_up'], data['thumbs_down']))
        self.conn.commit()

    def close(self):
        self.c.close()
        self.conn.close()


def pythonInserts(numIter):

    db = UrbanSQLite("data/urbanlitet.sqlite")
    db.create()
    with open('words.json', 'r', encoding="utf8") as jsonFile:
        i = 0
        for line in jsonFile:
            if (i >= numIter):
                break
            data = json.loads(line)
            db.insert(data)
            i += 1
    db.close()

def pd_np_inserts(numIter):

    a = np.empty((0, 3), object)
    with open('words.json', 'r', encoding="utf8") as jsonFile:
        i = 0
        for line in jsonFile:
            if (i >= numIter):
                break
            data = json.loads(line)
            arr_data = [[data["lowercase_word"], data['thumbs_up'], data['thumbs_down']]]

            a = np.append(a, arr_data, axis=0)
            i += 1
    df = pd.DataFrame(a, columns=["lowercase_word", "thumbs_up", "thumbs_down"])

    conn = sqlite3.connect("data/urbanlitet2.sqlite")

    df.to_sql("per_word", conn, if_exists='replace', index=False,
              dtype={"lowercase_word": "TEXT", "thumbs_up": "INTEGER", "thumbs_down": "INTEGER"})

def list_inserts(numIter):

    a = []
    with open('words.json', 'r', encoding="utf8") as jsonFile:
        i = 0
        for line in jsonFile:
            if (i >= numIter):
                break
            data = json.loads(line)
            arr_data = [data["lowercase_word"], data['thumbs_up'], data['thumbs_down']]

            a.append(arr_data)
            i += 1

    df = pd.DataFrame(a, columns=["lowercase_word", "thumbs_up", "thumbs_down"])

    conn = sqlite3.connect("data/urbanlitet3.sqlite")

    df.to_sql("per_word", conn, if_exists='replace', index=False,
              dtype={"lowercase_word": "TEXT", "thumbs_up": "INTEGER", "thumbs_down": "INTEGER"})

def list_inserts_main(output_file, input_files, retrieved_data_names, data_types):

    aggregate_arr = []
    for file in input_files:
        print("on file: " + file)
        aggregate_arr = aggregate_arr + list_inserts_to_array(file, retrieved_data_names)

    df = pd.DataFrame(aggregate_arr, columns=retrieved_data_names)

    conn = sqlite3.connect("data/%s" % output_file)
    dt = dict()
    for i in range(0, len(retrieved_data_names)):
        dt[retrieved_data_names[i]] = data_types[i]
    df.to_sql("per_word", conn, if_exists='replace', index=False,
              dtype=dt)

def list_inserts_to_array(input_file, retrieved_data_names):
    a = []
    with open(input_file, 'r', encoding="utf8") as jsonFile:
        i = 0
        start = time.time()
        for line in jsonFile:
            if (i % 50000 == 0):
                print(i)
                print("list inserts %s" % (time.time() - start))
            try:
                data = json.loads(line)
            except:
                print("error encountred, skipping data")
            arr_data = []
            for name in retrieved_data_names:
                try:
                    arr_data.append(data[name])
                except KeyError as e:
                    arr_data.append("-1")

            a.append(arr_data)
            i += 1
    return a

def benchmark(numIter):

    start = time.time()
    pythonInserts(numIter)
    print("db inserts %s" % (time.time() - start))


    start = time.time()
    pd_np_inserts(numIter)
    print("numpy inserts %s" % (time.time() - start))

    # does better on bigger data
    start = time.time()
    list_inserts(numIter)
    print("list inserts %s" % (time.time() - start))


def __init__():
    #list_inserts_main("urbanlitet_main.sqlite", "words.json", ["lowercase_word", 'thumbs_up', 'thumbs_down'])
    # list_inserts_main("reddit_temp.sqlite", "RC_2005-12.json",
    #                   ["body", 'score', 'ups', "gilded", "controversiality", "subreddit"],
    #                   ["TEXT", "INTEGER", 'INTEGER', 'INTEGER', 'INTEGER', "TEXT"])

    list_inserts_main("reddit_submissions_2011.sqlite", ["RS_2011-01.json", "RS_2011-02.json", "RS_2011-03.json",
                                             "RS_2011-04.json", "RS_2011-05.json", "RS_2011-06.json",
                                             "RS_2011-07.json", "RS_2011-08.json", "RS_2011-09.json",
                                             "RS_2011-10.json", "RS_2011-11.json", "RS_2011-12.json"],
                      ["title", 'score', 'ups', "num_comments", "distinguished", "subreddit", "author"],
                      ["TEXT", "INTEGER", 'INTEGER', 'INTEGER', 'TEXT', "TEXT", "TEXT"])

__init__()