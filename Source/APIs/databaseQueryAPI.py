import sqlite3
import os

def query_database(database_name, query, **kwargs):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, "..", "Databases", database_name)

    params = kwargs.get('params', None)

    con = sqlite3.connect(full_path)
    cur = con.cursor()

    if params is None:
        result = cur.execute(query)
    else:
        result = cur.execute(query, params)
    con.commit()
    return result
