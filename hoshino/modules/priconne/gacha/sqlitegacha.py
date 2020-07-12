import sqlite3
import os
import time
import pickle

from hoshino import logger
from .exception import DatabaseError

DB_PATH = os.path.expanduser('~/.hoshino/collections.db')

class SqliteGacha(object):

    def __init__(self):
        self._dbpath = DB_PATH
        self._columns = 'uid,colle,jewel,hiishi'
        self._fields = '''
        uid INT PRIMARY KEY NOT NULL,
        colle BLOB NOT NULL,
        jewel INT NOT NULL,
        hiishi INT NOT NULL
        '''
        self._create_sql()
    

    def _create_sql(self):
        sql = "CREATE TABLE IF NOT EXISTS Colle ({0})".format(self._fields)
        with self._connect() as conn:
            conn.execute(sql)

    def _connect(self):
        return sqlite3.connect(self._dbpath, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    
    @staticmethod
    def row2item(r):
        return {'uid': r[0], 'colle': r[1], 'jewel': r[2], 'hiishi': r[3]} if r else None
    
    def add(self, character):
        with self._connect() as conn:
            try:
                conn.execute('''
                INSERT INTO Colle ({0}) VALUES (?, ?, ?,?)
                '''.format(self._columns),
                (character['uid'], character['colle'], character['jewel'], character['hiishi']))
            except (sqlite3.DatabaseError) as e:
                logger.error(f'[Gacha.add]{e}')
                raise DatabaseError('创建仓库失败')
    
    def modify(self,character):
        with self._connect() as conn:
            try:
                conn.execute('''
                UPDATE Colle SET colle=?,jewel=?,hiishi=? WHERE uid=?
                ''',
                (character['colle'], character['jewel'], character['hiishi'], character['uid']))
            except (sqlite3.DatabaseError) as e:
                logger.error(f'[Gacha.modify]{e}')
                raise DatabaseError('修改仓库失败')
    
    def find_one(self, uid):
        with self._connect() as conn:
            try:
                ret = conn.execute('''
                    SELECT {0} FROM Colle WHERE uid=?
                    '''.format(self._columns),
                    (uid,)).fetchone()
                return self.row2item(ret)
            except (sqlite3.DatabaseError) as e:
                logger.error(f'[Gacha.find_one]{e}')
                raise DatabaseError('查找仓库失败')
                
        
            
