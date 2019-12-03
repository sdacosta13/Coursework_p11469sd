import sqlite3
"""
Written By Sam da Costa
Used to return the data from the db
"""


def connect():
    conn = sqlite3.connect("status")
    cur = conn.cursor()
    return conn, cur


def query(userName):
    conn, cur = connect()
    query = "SELECT shotAmmo, mgAmmo, zombLevel FROM setting WHERE pName = \"{}\"".format(userName)
    data = cur.execute(query)
    data = cur.fetchall()
    return data


def update(pName, shotAmmo, mgAmmo, zombLevel):
    conn, cur = connect()
    query = "INSERT INTO setting (pName, shotAmmo, mgAmmo, zombLevel) VALUES (\"{}\",{},{},{})".format(
        pName, shotAmmo, mgAmmo, zombLevel)
    cur.execute(query)
