import sqlite3
import os

from Source.Constants.constants import DATABASE_FILE_NAME


def query_database(query, **kwargs):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, "..", "Databases", DATABASE_FILE_NAME)

    params = kwargs.get('params', None)

    con = sqlite3.connect(full_path)
    con.execute("PRAGMA foreign_keys = ON")  # Enable foreign keys
    cur = con.cursor()

    if params is None:
        result = cur.execute(query)
    else:
        result = cur.execute(query, params)
    con.commit()
    return result, con
