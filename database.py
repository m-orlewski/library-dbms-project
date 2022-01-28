import psycopg2
import os
import urllib.parse

def connectToDatabase():
    urllib.parse.uses_netloc.append("postgres")
    url = urllib.parse.urlparse("postgres://dnahfzon:qXIKAdro1glx68jGYpWCigc4C69EzbSH@ella.db.elephantsql.com/dnahfzon")

    try:
        conn = psycopg2.connect(
            database = url.path[1:],
            user = url.username,
            password = url.password,
            host = url.hostname,
            port = url.port
        )
    except:
        print("connectToDatabase exception")
        conn = None

    return conn
