import psycopg2
import psycopg2.extras
from dbutils.pooled_db import PooledDB
from config.local_settings import DATABASE, HEALTH_DATABASE


def db_conn(func):
    '''
    decorator function for DB connection
    '''
    def wrapper(*args, **kwargs):
        try:
            conn = HEALTH_DB.connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            result = func(*args, **kwargs, cursor=cursor)

            return True, result
        except Exception as e:
            print("Error, {}() : {}".format(func.__name__, e))

            return False, None
        finally:
            cursor.close()
            conn.commit()
            conn.close()

    return wrapper


# Connect to health Database
try:
    HEALTH_DB = PooledDB(
        creator=psycopg2,
        mincached=DATABASE['mincached'],
        maxconnections=DATABASE['maxconnections'],
        blocking=True,
        host=HEALTH_DATABASE['host'],
        port=HEALTH_DATABASE['port'],
        user=HEALTH_DATABASE['id'],
        password=HEALTH_DATABASE['pw'],
        dbname=HEALTH_DATABASE['db'],
        connect_timeout=DATABASE['connect_timeout'],
        ping=DATABASE['ping'],
    )
    print("CONNECT!!")
except Exception as e:
    msg = "[Emergency Error] service cannot connect to PostgreSQL - \
           [host: {}, db: {}, error: {}]".format(HEALTH_DATABASE['host'], HEALTH_DATABASE['db'], e)
    print(msg)
