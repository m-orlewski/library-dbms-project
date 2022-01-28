from psycopg2 import connect
import urllib.parse

def connect_postgres():
    urllib.parse.uses_netloc.append("postgres")
    url = urllib.parse.urlparse("postgres://dnahfzon:qXIKAdro1glx68jGYpWCigc4C69EzbSH@ella.db.elephantsql.com/dnahfzon")
    print ("\nconnecting to PostgreSQL")
    try:
        conn = connect (
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    except Exception as err:
        print ("PostgreSQL Connect() ERROR:", err)
        conn = None

    return conn