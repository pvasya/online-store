import psycopg2
import config

class DAOBase:
    def __init__(self):
        self.conn = psycopg2.connect(**config.DB)
        self.cur = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()