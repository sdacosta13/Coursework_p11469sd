import sqlite3
"""
Written By Sam da Costa
Used to return the data from the db
"""


def connect():
    conn = sqlite3.connect("status2.db")
    cur = conn.cursor()
    return conn, cur


def query(userName):
    conn, cur = connect()
    query = "SELECT shotAmmo, mgAmmo, zombLevel, score FROM setting WHERE pName = ?"
    data = cur.execute(query, (userName,))
    data = cur.fetchall()
    return data[0]


def queryForNames():
    conn, cur = connect()
    query = "SELECT pName FROM setting"
    data = cur.execute(query).fetchall()
    return data


def update(pName, shotAmmo, mgAmmo, zombLevel, score):
    conn, cur = connect()
    query = "INSERT INTO setting (pName, shotAmmo, mgAmmo, zombLevel, score) VALUES (?,?,?,?,?)"
    cur.execute(query, (pName, shotAmmo, mgAmmo, zombLevel, score))
    conn.commit()


def getScores():
    conn, cur = connect()
    query = "SELECT pName, score FROM setting ORDER BY score DESC"
    data = cur.execute(query).fetchall()
    return data
