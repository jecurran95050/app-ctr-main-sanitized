from pg.pg_auth import *

__author__ = 'jacurran'


###################################################################################

def pg_create_connection(pg_pw=get_pg_pw(),
                         db_name="XXXXX",
                         pg_host=settings["pg_host"],
                         pg_port="XXXX"):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user="XXXXX",
            password=pg_pw,
            host=pg_host,
            port=pg_port,
        )
    except:
        pass
    return connection


def create_db(db_name, pg_pw=get_pg_pw(), pg_host=settings["pg_host"]):
    try:
        SQL = f'CREATE DATABASE "{db_name}";'
        connection = pg_create_connection(pg_pw=pg_pw, pg_host=pg_host)
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(SQL)
        connection.close()
        return True
    except:
        return False


def drop_db(db_name, pg_pw=get_pg_pw(), pg_host=settings["pg_host"]):
    try:
        SQL1 = f'SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname="{db_name}";'
        SQL2 = f'DROP DATABASE "{db_name}";'
        connection = pg_create_connection(pg_pw=pg_pw, pg_host=pg_host)
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(SQL1)
        cursor.execute(SQL2)
        connection.close()
        return True
    except:
        return False


def update_pg_pw(old_pw,new_pw, pg_host=settings["pg_host"]):
    SQL = f"""ALTER USER "XXXXX" WITH PASSWORD '{new_pw}'"""
    try:
        connection = pg_create_connection(pg_pw=old_pw, pg_host=pg_host)
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(SQL)
        connection.close()
        return True
    except:
        return False

###################################################################################

class DB:
    def __init__(self,
                 db_name,
                 pg_host=settings["pg_host"],
                 pg_pw=get_pg_pw(),
                 pg_port="XXXX"):

        self.db_name = db_name
        self.pg_host = pg_host
        self.pg_user = "XXXXXX"
        self.pg_pw = pg_pw
        self.pg_port = pg_port
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                database=self.db_name,
                user="XXXXX",
                password=self.pg_pw,
                host=self.pg_host,
                port=self.pg_port,
            )
        except:
            pass

    def close(self):
        if self.connection:
            self.connection.close()

    def wr_query(self, query):
        try:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query)
                self.connection.commit()
                return True
            except:
                self.connection.rollback()
                return False
        except:
            return False


    def ro_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except:
            return list()


    def drop_table(self, table):
        SQL = f"DROP TABLE IF EXISTS {table};"
        result = self.wr_query(query=SQL)
        return result


    def drop_table_cascade(self, table):
        SQL = f"DROP TABLE IF EXISTS {table} CASCADE;"
        result = self.wr_query(query=SQL)
        return result

###################################################################################

